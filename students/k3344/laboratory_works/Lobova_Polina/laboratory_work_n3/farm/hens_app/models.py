from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    passport = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.first_name} {self.second_name}"

class Workshop(models.Model):
    title = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.title}, вместимость {self.capacity}"

class Cell(models.Model):
    cell_code = models.CharField(max_length=100, primary_key=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    row = models.IntegerField()
    column = models.IntegerField()

    def __str__(self):
        return f" Клетка в цехе {self.workshop}, ряд {self.row}, колонка {self.column}"

class Diet(models.Model):
    description = models.CharField(max_length=100)
    seasons_choices = [
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
        ('AUTUMN', 'Autumn'),
        ('WINTER', 'Winter'),
    ]
    season = models.CharField(max_length=10, choices=seasons_choices)

    def __str__(self):
        return f"{self.get_season_display()}"

class ResponsibleEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee} следит за клеткой {self.cell}"

class Breed(models.Model):
    name = models.CharField(max_length=50)
    egg_performance_avg = models.IntegerField()
    weight_avg = models.FloatField()
    diet_num = models.ForeignKey(Diet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Chicken(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)
    weight = models.FloatField()
    age = models.IntegerField()
    egg_performance_month = models.IntegerField()

    def __str__(self):
        return f" Курица породы {self.breed} в клетке {self.cell}, {self.egg_performance_month} яйц в месяц, "

class Contract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    contract_statuses = [
        ('a', 'active'),
        ('f', 'fired'),
    ]
    contract_types = [
        ('f', 'full-time'),
        ('p', 'part-time')
    ]
    type = models.CharField(max_length=10, choices=contract_types)
    status = models.CharField(max_length=10, choices=contract_statuses)
    salary = models.IntegerField()

    def __str__(self):
        return f" Контракт {self.employee} статус: {self.get_status_display()}"






