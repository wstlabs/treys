from treys.lookup import LookupTable
from treys.util.io import write_table

# create an evaluator
# evaluator = Evaluator()
# t = evaluator.table
t = LookupTable()
print("btw ..")
write_table(t.flush,"out/flush.txt")
write_table(t.unsuited,"out/unsuited.txt")
print("all done")

