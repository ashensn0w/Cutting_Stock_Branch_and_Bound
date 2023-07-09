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
                    print(f"Demand {i+1}: Cut {demand} length {cuts} times")
            print("Total Waste:", self.calculate_total_waste(), "length")
        else:
            print("No feasible solution found.")
    
    def branch_and_bound(self, state):
        current_solution, remaining_length, current_waste = state
        
        if sum(current_solution) == self.num_demands:
            if current_waste < self.best_waste:
                self.best_solution = current_solution[:]
                self.best_waste = current_waste
            return
        
        if remaining_length < min(self.demands):
            return
        
        for i in range(self.num_demands):
            if current_solution[i] < 1:
                demand = self.demands[i]
                max_cuts = remaining_length // demand
                
                for cuts in range(max_cuts, -1, -1):
                    updated_solution = current_solution[:]
                    updated_solution[i] += cuts
                    updated_waste = current_waste + (remaining_length - cuts * demand)
                    updated_state = (updated_solution, remaining_length - cuts * demand, updated_waste)
                    
                    self.branch_and_bound(updated_state)
                    
                    if self.best_solution is not None:
                        return

    def calculate_total_waste(self):
        total_waste = 0
        total_cuts = 0
        for i in range(self.num_demands):
            demand = self.demands[i]
            cuts = self.best_solution[i]
            total_cuts += cuts * demand
        total_waste =  self.stock_length - total_cuts
        return total_waste

# Example usage:
if __name__ == "__main__":
    stock_length = int(input("Enter the stock length: "))
    num_demands = int(input("Enter the number of demands: "))
    demands = []
    for i in range(num_demands):
        demand = int(input("Enter the length to be cut for demand " + str(i+1) + ": "))
        demands.append(demand)
    
    demands = sorted(demands, reverse=True)  # Sort demands in descending order
    
    problem = CuttingStockProblem(stock_length, demands)
    problem.solve()
