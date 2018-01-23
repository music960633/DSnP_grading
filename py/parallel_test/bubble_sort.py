#!/usr/bin/python2.7

import time
import random

def random_arr(n):
  arr = []
  for i in range(n):
    arr.append(random.random())
  return arr


def bubble_sort(a):
  arr = list(a)
  n = len(arr)
  for i in range(n-1, 0, -1):
    for j in range(i):
      if arr[j] > arr[j+1]:
        arr[j], arr[j+1] = arr[j+1], arr[j]
  return arr


def check_sort(n):
  arr1 = random_arr(n)
  arr2 = list(arr1)
  arr1 = bubble_sort(arr1)
  arr2 = sorted(arr2)
  assert arr1 == arr2, 'Bubble sort error!!'


def main():
  st = time.time()
  check_sort(5000)
  ed = time.time()
  print ed - st


if __name__ == '__main__':
  main()
