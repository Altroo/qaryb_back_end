from django.db.models.functions import Coalesce
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from places.base.filters import UserLanguageMixin, CountryFilterSet, CityFilterSet, BaseAllCountryFilter
from places.base.serializers import BaseCountrySerializer, BaseCitySerializer, BaseCountriesSerializer
from places.base.choices import PlaceType
from places.models import Country, City

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from places.base.language_cleaner import LanguageCleaner
from places.base.nominatim import NominatimSearch


class PlaceLanguageMixin(UserLanguageMixin):
    """
    Mixin of places
    """

    permission_classes = (AllowAny,)

    def get_queryset(self):
        return super().get_queryset() \
            .annotate(language_name=Coalesce(f'name_{self.user_language.lower()}', 'name')) \
            .defer('name').exclude(language_name__exact='').order_by('language_name')


class CountriesListView(PlaceLanguageMixin, ListAPIView):
    """
    List of countries
    """

    permission_classes = (AllowAny,)
    queryset = Country.objects.filter(cities__isnull=False, type=PlaceType.COUNTRY).distinct()\
        .exclude(code='').order_by('name_fr')
    serializer_class = BaseCountrySerializer
    filterset_class = CountryFilterSet
    pagination_class = None

    def get_queryset(self):
        if not self.request.GET.get('all'):
            return super().get_queryset()
        else:
            self.filterset_class = BaseAllCountryFilter
            self.serializer_class = BaseCountriesSerializer
            return Country.objects.all().distinct().exclude(code='').order_by('name_fr')


class CountryCodesListView(APIView):
    """
       List of countries
       """
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request, *args, **kwargs):
        queryset = Country.objects.filter(type=PlaceType.COUNTRY).exclude(code='') \
            .distinct().order_by('code').values_list('code', flat=True)
        return Response(queryset)


class CitiesListView(PlaceLanguageMixin, ListAPIView):
    """
    List of countries
    """
    permission_classes = (permissions.AllowAny,)
    queryset = City.objects.all()
    serializer_class = BaseCitySerializer
    filterset_class = CityFilterSet
    pagination_class = None

    def get_queryset(self):
        if not self.request.GET.get('code'):
            return self.queryset.model.objects.none()
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for obj in serializer.data:
            for k, v in obj.items():
                if v == 'Tout le maroc':
                    data.insert(0, v)
                elif v == 'Les autres villes':
                    data.insert(0, v)
                else:
                    data.append(v)
        # return Response({'name_tag': data})
        return Response(data=data, status=status.HTTP_200_OK)


class GetLocalisationNameView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request, *args, **kwargs):
        lang = 'FR'
        port = '7079'
        long = float(kwargs.get('lon'))
        lat = float(kwargs.get('lat'))
        try:
            clean_result = NominatimSearch(language=lang, port=port) \
                .get_name_of_place(lat=lat, long=long, additional_info=True)[0].get('address')
            needed_keys = ['commercial', 'road', 'industrial', 'neighbourhood', 'suburb',
                           'city_district', 'hamlet', 'town', 'village',
                           'county', 'residential', 'city']

            final_result = None
            for i in needed_keys:
                result = clean_result.get(i)
                if result is not None:
                    final_result = result
                    break

            if final_result is None:
                errors = {"error": ["The given geo is not a valid road!"]}
                raise ValidationError(errors)

            clean_result = LanguageCleaner().clear_string(final_result, 'tifinagh',
                                                          {'tifinagh': {'start': 'u2d30', 'end': 'u2d7f'}})

            data = {'localisation_name': clean_result}
            return Response(data=data, status=status.HTTP_200_OK)

        except (IndexError, AttributeError):
            errors = {"error": ["The given geo is not a valid road!"]}
            raise ValidationError(errors)
