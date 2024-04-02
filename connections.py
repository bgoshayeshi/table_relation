import json
from collections import defaultdict, deque

# Load JSON files (assuming these contain the schema you've described)
with open('table_dictionary.json', 'r') as file:
    table_dict = json.load(file)
with open('column_dictionary.json', 'r') as file:
    column_dict = json.load(file)

from collections import defaultdict, deque

# Assuming the structure of table_dict and column_dict as previously defined

# Create a directed graph where each edge represents a possible move from one table to another via a shared column
graph = defaultdict(list)
for col, tbls in column_dict.items():
    for i, tbl in enumerate(tbls):
        for otbl in tbls[i+1:]:
            graph[tbl].append((otbl, col))
            graph[otbl].append((tbl, col))



# BFS to find paths while ensuring valid table-to-table transitions
def find_valid_paths(start_column, end_column):
    # Initialize the queue with tables containing the start column
    start_tables = column_dict[start_column]
    visited = set()
    queue = deque([(table, [(table, start_column)]) for table in start_tables])

    valid_paths = []

    while queue:
        current_table, path = queue.popleft()

        if (current_table, path[-1][1]) in visited:  # Skip if this table-column pair was already visited
            continue
        visited.add((current_table, path[-1][1]))

        # Check if the current path has reached a table with the end column
        if end_column in table_dict[current_table]:
            valid_paths.append(path + [(current_table, end_column)])
            continue

        # Explore adjacent tables that have a shared column
        for next_table, shared_column in graph[current_table]:
            if all(p[0] != next_table for p in path):  # Prevent looping back to already visited tables in this path
                queue.append((next_table, path + [(next_table, shared_column)]))

    return valid_paths

def generate_sql_from_path(path, start_column, end_column):
    if not path or len(path) < 2:
        return "Path is too short to generate a meaningful query."
    
    # Start building the SELECT part of the SQL query
    sql = f"SELECT {path[0][0]}.{start_column}, {path[-1][0]}.{end_column} "
    
    # Add the FROM part of the SQL query
    sql += f"FROM {path[0][0]} "
    
    # Iteratively build the JOIN part of the SQL query
    for i in range(1, len(path)):
        prev_table, prev_col = path[i-1]
        current_table, join_col = path[i]
        
        # Assuming many-to-many, a typical representation would involve an intermediary table
        # This simple model does not account for that complexity and assumes direct join for simplicity
        sql += f"JOIN {current_table} ON {prev_table}.{prev_col} = {current_table}.{join_col} "
    
    return sql


start_column = 'A1'
end_column = 'D1'
valid_paths = find_valid_paths(start_column, end_column)

# Simplify the output for clarity
for path in valid_paths:
    simplified_path = ' -> '.join([f"{table} via {col}" for table, col in path])
    print(simplified_path)
    print(generate_sql_from_path(path, start_column, end_column))