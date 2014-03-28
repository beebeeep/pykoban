import copy


def test(a):
  v = copy.deepcopy(a)
  (b,x) = v

  b[0][0] = -1;
  for r in b:
    for c in r:
      c = 2

a = [[1,2,3],[4,5,6],[7,8,9]]
print a
test((a, 1))
print a
