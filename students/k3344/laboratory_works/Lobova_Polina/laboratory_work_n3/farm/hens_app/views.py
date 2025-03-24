from django.db.models import Avg, Count, Sum, Q

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workshop, Cell, Employee, ResponsibleEmployee, Breed, Chicken, Diet, Contract
from .serializers import (EmployeeSerializer, ResponsibleEmployeeSerializer,
                         DietSerializer, BreedSerializer, ChickenSerializer,
                         ContractSerializer, CellSerializer, ResponsibleEmployeeWriteSerializer,
                         BreedWriteSerializer, ChickenWriteSerializer, ContractWriteSerializer,
                         CellWriteSerializer)


class EmployeeAPIView(GenericAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()


class ResponsibleEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResponsibleEmployeeWriteSerializer

    def get(self, request):
        employees = ResponsibleEmployee.objects.all()
        serializer = ResponsibleEmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResponsibleEmployeeWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResponsibleEmployeeDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResponsibleEmployeeWriteSerializer
    permission_classes = [IsAuthenticated]
    queryset = ResponsibleEmployee.objects.all()


class DietAPIView(GenericAPIView):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        diets = Diet.objects.all()
        serializer = DietSerializer(diets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DietSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DietDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]
    queryset = Diet.objects.all()


class BreedAPIView(GenericAPIView):
    serializer_class = BreedWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BreedWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BreedDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BreedWriteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Breed.objects.all()


class ChickenAPIView(GenericAPIView):
    serializer_class = ChickenWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chickens = Chicken.objects.all()
        serializer = ChickenSerializer(chickens, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChickenWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChickenDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChickenWriteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Chicken.objects.all()


class ContractAPIView(GenericAPIView):
    serializer_class = ContractWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContractWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContractWriteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contract.objects.all()


class CellAPIView(GenericAPIView):
    serializer_class = CellWriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cells = Cell.objects.all()
        serializer = CellSerializer(cells, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CellWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Ответы на вопросы из текста лабораторной работы

class EggPerformanceByAgeBreedWeightAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Какое количество яиц получают от каждой курицы данного веса, породы, возраста?",
        manual_parameters=[
            openapi.Parameter(
                'weight',
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description='Вес',
                required=True,
            ),
            openapi.Parameter(
                'breed_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Идентификатор породы',
                required=True,
            ),
            openapi.Parameter(
                'age',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Возраст',
                required=True,
            )
        ],
        responses={
            200: openapi.Response(description='Info retrieved'),
        }
    )

    def get(self, request):
        weight, breed_id, age = request.query_params.get('weight'), request.query_params.get('breed_id'), request.query_params.get('age')

        chickens = Chicken.objects.filter(weight=weight, breed_id=breed_id, age=age)
        total_eggs = chickens.aggregate(Sum('egg_performance_month'))['egg_performance_month__sum'] or 0
        count = chickens.count()
        eggs_per_chicken = total_eggs / count if count > 0 else 0

        return Response({"Количество яиц от курицы": eggs_per_chicken}, status=status.HTTP_200_OK)


class WorkshopWithMostBreedsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="В каком цехе наибольшее количество кур определенной породы?",
        manual_parameters=[
            openapi.Parameter(
                'breed_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Идентификатор породы',
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description='Info retrieved'),
        }
    )

    def get(self, request):
        breed_id = request.query_params.get('breed_id')
        workshop = Workshop.objects.annotate(
            breed_count=Count('cell__chicken', filter=Q(cell__chicken__breed_id=breed_id))
        ).order_by('-breed_count').first()

        return Response({
            "Цех": workshop.title if workshop else "Нет информации",
            "Количество куриц одной породы в цехе": workshop.breed_count if workshop else 0
        }, status=status.HTTP_200_OK)


class AverageEggsPerEmployeeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Среднее количество яиц, которое получает в день каждый работник от обслуживаемых им кур?",
        responses={
            200: openapi.Response(description='Info retrieved'),
        }
    )

    def get(self, request):
        employees = Employee.objects.annotate(
            total_eggs=Sum('responsibleemployee__cell__chicken__egg_performance_month'),
            chicken_count=Count('responsibleemployee__cell__chicken')
        ).filter(chicken_count__gt=0)

        data = [
            {
                "работник": f"{employee.first_name} {employee.second_name} {employee.middle_name}",
                "среднее количество яиц за день": round(employee.total_eggs / 30, 2) if employee.total_eggs > 0 else 0
            }
            for employee in employees
        ]
        return Response(data, status=status.HTTP_200_OK)


class ChickenCountByBreedWorkshopAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Сколько кур каждой породы в каждом цехе?",
        responses={
            200: openapi.Response(description='Info retrieved'),
        }
    )

    def get(self, request):
        data = Cell.objects.values(
            'workshop__title', 'chicken__breed__name'
        ).annotate(chicken_count=Count('chicken'))

        response_data = [
            {
                "Цех": entry["workshop__title"],
                "Название породы": entry["chicken__breed__name"],
                "Количество куриц": entry["chicken_count"],
            }
            for entry in data
        ]
        return Response(response_data, status=status.HTTP_200_OK)


class BreedPerformanceDifferenceAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Какова для каждой породы разница между показателями породы и средними показателями по птицефабрике?",
        responses={
            200: openapi.Response(description='Info retrieved'),
        }
    )

    def get(self, request):
        overall_avg = Chicken.objects.aggregate(
            avg_eggs=Avg('egg_performance_month'), avg_weight=Avg('weight')
        )

        breeds = Breed.objects.annotate(
            avg_eggs=Avg('chicken__egg_performance_month'),
            avg_weight=Avg('weight_avg')
        ).values('name', 'avg_eggs', 'avg_weight')

        data = [
            {
                "Порода": breed['name'],
                "Разница в количестве яиц": int(breed['avg_eggs'] - overall_avg['avg_eggs']) if overall_avg['avg_eggs'] and breed['avg_eggs'] is not None else 0,
                "Разница в весе": round(breed['avg_weight'] - overall_avg['avg_weight'], 2) if overall_avg['avg_weight'] and breed['avg_weight'] is not None else 0
            }
            for breed in breeds
        ]
        return Response(data, status=status.HTTP_200_OK)


class MonthlyReportAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_month_data = Chicken.objects.values('cell__workshop__title', 'breed__name').annotate(
            total_eggs=Sum('egg_performance_month'),
            chicken_count=Count('id'),
            avg_performance=Avg('egg_performance_month')
        )

        overall_stats = Chicken.objects.aggregate(
            total_chickens=Count('id'), total_eggs=Sum('egg_performance_month')
        )

        report = {
            "last_month_data": [
                {
                    "Цех": data['cell__workshop__title'],
                    "Название породы": data['breed__name'],
                    "Количество куриц": data['chicken_count'],
                    "Всего яиц": data['total_eggs'],
                    "Средняя производительность": data['avg_performance']
                }
                for data in last_month_data
            ],
            "Показатели": overall_stats
        }

        return Response(report, status=status.HTTP_200_OK)

