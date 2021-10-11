import time as tm
import solver as sv

cubestring = 'UUFUUFUUFRRRRRRRRRFFDFFDFFDDDBDDBDDBLLLLLLLLLUBBUBBUBB'
#cubestring = input()

start = tm.time()
a = sv.solve(cubestring, 18, 0.1)
end = tm.time()

print(a)
print(end - start)
quit()
