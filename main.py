import math

class CuttingStockProblem:
    def __init__(self, stock_length, demands):
        self.stock_length = stock_length
        self.demands = demands
        self.num_demands = len(demands)
        self.best_solution = None
        self.best_waste = math.inf
    
    def solve(self):
        initial_state = ([0] * self.num_demands, self.stock_length, 0)
        self.branch_and_bound(initial_state)
        
        if self.best_solution is not None:
            print("Optimal Solution Found:")
            for i in range(self.num_demands):
                demand = self.demands[i]
                cuts = self.best_solution[i]
                if cuts > 0:
                    print(f"Cut {demand} length {cuts} times")
            print("Total Waste:", self.best_waste)
        else:
            print("No feasible solution found.")
    
    def branch_and_bound(self, state):
        current_solution, remaining_length, current_waste = state
        
        if remaining_length < min(self.demands):
            if current_waste < self.best_waste:
                self.best_solution = current_solution[:]
                self.best_waste = current_waste
            return
        
        if current_waste >= self.best_waste:
            return
        
        for i in range(self.num_demands):
            demand = self.demands[i]
            max_cuts = remaining_length // demand
            
            for cuts in range(max_cuts, -1, -1):
                updated_solution = current_solution[:]
                updated_solution[i] += cuts
                updated_waste = current_waste + (remaining_length - cuts * demand)
                updated_state = (updated_solution, remaining_length - cuts * demand, updated_waste)
                
                self.branch_and_bound(updated_state)

# Example usage:
if __name__ == "__main__":
    stock_length = int(input("Enter the stock length: "))
    num_demands = int(input("Enter the number of demands: "))
    demands = []
    for i in range(num_demands):
        demand = int(input("Enter the length to be cut for demand " + str(i+1) + ": "))
        demands.append(demand)
    
    problem = CuttingStockProblem(stock_length, demands)
    problem.solve()
