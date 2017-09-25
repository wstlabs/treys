
def write_table(table, filepath):
    """Writes a lookup table to a file."""
    with open(filepath, 'wt') as f:
        for k,v in table.items():
            f.write(str(k)+","+str(v)+'\n')

