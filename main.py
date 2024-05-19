import math
import numpy as np
import random
import matplotlib.pyplot as plt
from statistics import mode
#Сканирование выборки из файла
def scan_file(filename):
    numbers = []
    with open(filename, "r") as file:
        for line in file:
            try:
                num = float(line.strip())
                numbers.append(num)
            except ValueError:
                print(f"Ignoring invalid number")
    return numbers

list_elem = scan_file("var_9.csv")

#Количество значений в выборке
def size_sample(numbers):
    len=0
    for i in numbers:
        len+=1
    return len

#Сумма элементов выборки
def numbers_sum(numbers):
    total_sum=0
    for num in numbers:
        total_sum+=num
    return total_sum

#Выборочное среднее
def sample_mean(numbers):
    total_sum=numbers_sum(numbers)
    len=size_sample(numbers)
    if len==0:
        return -1
    return total_sum/len

def quick_sort(numbers):
    if sample_mean(numbers) <= 1:
        return numbers
    
    # Выбираем опорный элемент (pivot)
    pivot = numbers[0]
    
    # Разделяем список на элементы меньше, равные и больше опорного
    left = [i for i in numbers[1:] if i <= pivot]
    right = [i for i in numbers[1:] if i > pivot]
    
    # Рекурсивно сортируем левую и правую части
    return quick_sort(left) + [pivot] + quick_sort(right)

#Медиана
def get_median(numbers):
    numbers=quick_sort(numbers)
    n = size_sample(numbers)
    
    if n % 2 == 0:  
        mid1 = numbers[n // 2 - 1]
        mid2 = numbers[n // 2]
        median = (mid1 + mid2) / 2
    else:  
        median = numbers[n // 2]
    
    return median

#Максимум
def find_maximum(numbers):
    if size_sample(numbers) == 0:
        return None
    max_value = numbers[0]
    for i in range(1, size_sample(numbers)):
        if numbers[i] > max_value:
            max_value = numbers[i]
    return max_value

#Минимум
def find_minimum(numbers):
    if size_sample(numbers) == 0:
        return None
    min_value = numbers[0]
    for i in range(1, size_sample(numbers)):
        if numbers[i] < min_value:
            min_value = numbers[i]
    return min_value

#Максимум из отсортированного списка
def get_max(numbers,len):
    return numbers[len-1]

#Минимум из отсортированного списка
def get_min(numbers):
    return numbers[0]

#Мода
def get_mode(numbers):
    frequency_dict = {}
    for value in numbers:
        if value in frequency_dict:
            frequency_dict[value] += 1
        else:
            frequency_dict[value] = 1
    max_frequency = find_maximum(list(frequency_dict.values()))    
    if max_frequency == 1:
        return None
    mode = [key for key, value in frequency_dict.items() if value == max_frequency]
    return mode

#Размах выборки
def get_sample_range(max, min):
    return (max - min)

#Смещенная дисперсия
def get_biased_variance(len, sample_mean, numbers):
    variance=0
    if len == 0:
        return 0
    for x in numbers:
        variance+=(x - sample_mean) ** 2
    variance/=len
    return variance

#Несмещенная дисперсия
def get_unbiased_variance(len,sample_mean,numbers):
    variance=0
    if len == 0:
        return 0
    for x in numbers:
        variance+=(float(x) - sample_mean) ** 2
    variance/=len-1
    return variance

#Выборочный начальный момент k-ого порядка 
def calculate_sample_raw_moment(numbers, k,len):
    if len == 0:
        return 0
    moment=0
    for x in numbers:
        moment+=x**k
    moment/=len
    return moment
#Выборочный центральный момент k-го порядка
def calculate_sample_central_moment(numbers, sample_mean,k,len):
    moment=0
    for x in numbers:
        moment+=(x-sample_mean)**k
    moment/=len
    return moment
def get_sample_central_moment1(data, len, sample_mean, k=3):
    if len == 0:
        return 0
    central_moment = get_sum((x - sample_mean) ** k for x in data) / len
    return central_moment

#Результаты выполнения функций

len=size_sample(list_elem)#Количество элементов в выборке
total_sum=numbers_sum(list_elem)#Сумма элементов в выборке
sample_mean1=sample_mean(list_elem)#Выборочное среднее
median=get_median(list_elem)#Медиана
moda=get_mode(list_elem)#мода
sorting_list_elem=quick_sort(list_elem)
max_value=get_max(sorting_list_elem,len)
min_value=get_min(sorting_list_elem)
sample_range=get_sample_range(max_value,min_value)#Размах выборки
unbiased_variance=get_unbiased_variance(len,sample_mean1,list_elem)#Несмещенная дисперсия
biased_variance=get_biased_variance(len,sample_mean1,list_elem)#Смещенная дисперсия
sample_raw_moment=calculate_sample_raw_moment(list_elem,3,len)#Выборочный начальный момент 3-ого порядка 
sample_central_moment=calculate_sample_central_moment(list_elem, sample_mean1,3,len)#Выборочный центральный момент 3-го порядка

print(f"Количество элементов в выбокрке={len}")
print(f"Сумма элементов в выборке={total_sum}")
print(f"Выборочное среднее={sample_mean1}")
print(f"Медиана={median}")
print(f"Мода={moda}")
print(f"Размах выборки={sample_range}")
print(f"Несмещенная дисперсия={unbiased_variance}")
print(f"Смещенная дисперсия={biased_variance}")
print(f"Выборочный начальный момент 3-ого порядка ={sample_raw_moment}")
print(f"Выборочный центральный момент 3-го порядка ={sample_central_moment}")


#Выбираем случайные элементы из выборки
def select_random_elements(data,k):
    random_elements = random.sample(data, k)
    return random_elements

#Построение гистограммы
def build_hist(sample,n):
    sample=quick_sort(sample)
    min_v=get_min(sample)
    max_v=get_max(sample,n)
    razmah=get_sample_range(max_v,min_v)
    num_bins =int(1 + 3.332*math.log(n))
    width=float(razmah/num_bins)
    plt.hist(sample, bins=num_bins, density=True, edgecolor='black')
    plt.xlabel('Частичные интервалы')
    plt.ylabel('Относительные частоты')
    plt.title(f"Гистограмма относительно частот для подвыборки из {n} элементов")
    plt.show()

sample_10=select_random_elements(list_elem,10)
sample_100=select_random_elements(list_elem,100)
sample_300=select_random_elements(list_elem,300)

build_hist(sample_300,10)
build_hist(sample_300,100)
build_hist(sample_300,300)
