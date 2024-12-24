import numpy
#########################################
#      Christmas Tree                   #
#########################################

x = numpy.arange(7, 16)
y = numpy.arange(1, 18, 2)
z = numpy.column_stack((x[:: -1], y))

for i, j in z:
    print(" "*i + '*' *j)

for r in range(3):
    print(" "*13, ' || ')

print(" "*12, end="\======/")
print("")

### SHOULD PRINT
#         *
#        ***
#       *****
#      *******
#     *********
#    ***********
#   *************
#  ***************
# *****************
#         || 
#         || 
#         || 
#      \======/
