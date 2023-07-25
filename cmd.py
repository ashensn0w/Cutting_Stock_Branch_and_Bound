import math
import heapq

class CuttingStockSolver:
    def __init__(self, stock_length, items):
        self.stock_length = stock_length
        self.items = items
        self.num_items = len(items)
        self.best_solution = None
        self.best_waste = math.inf
    
    def branch_and_bound_solve(self):
        initial_state = ([0] * self.num_items, self.stock_length, 0, 0, [0] * self.num_items)
        heap = []
        heapq.heappush(heap, initial_state)
        
        while heap:
            current_solution, remaining_length, current_waste, index, cuts_per_item = heapq.heappop(heap)
            
            if index == self.num_items:
                if remaining_length >= 0 and current_waste < self.best_waste:
                    self.best_solution = cuts_per_item[:]
                    self.best_waste = current_waste
                continue
            
            item_length = self.items[index]
            max_cuts = remaining_length // item_length
            
            for cuts in range(max_cuts, -1, -1):
                updated_solution = current_solution[:]
                updated_solution[index] += cuts
                updated_cuts_per_item = cuts_per_item[:]
                updated_cuts_per_item[index] += cuts
                updated_waste = remaining_length - cuts * item_length
                
                if updated_waste < self.best_waste:
                    updated_state = (updated_solution, remaining_length - cuts * item_length, updated_waste, index + 1, updated_cuts_per_item)
                    heapq.heappush(heap, updated_state)
        
    def print_solution(self):
        if self.best_solution is not None:
            print("Optimal Solution Found:")
            for i in range(self.num_items):
                item_length = self.items[i]
                cuts = self.best_solution[i]
                if cuts > 0:
                    print(f"Item {i+1}: Cut {item_length} length {cuts} times")
            print("Total Waste:", self.best_waste, "length")
        else:
            print("No feasible solution found.")

# Example usage:
if __name__ == "__main__":
    stock_length = int(input("Enter the stock length: "))
    num_items = int(input("Enter the number of items: "))
    items = []
    for i in range(num_items):
        item = int(input("Enter the length to be cut for demand " + str(i+1) + ": "))
        items.append(item)

    items = sorted(items, reverse=True)
    problem = CuttingStockSolver(stock_length, items)
    problem.branch_and_bound_solve()
    problem.print_solution()
