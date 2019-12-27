# Do not pass a list into this class... lists are mutable and repeated use of this class changes the list.
# An array is not mutable.
# Therefore pass an array into this class and it will get changed into a list in the instance.
class Kfold:
    def __init__(self, k, data_set):
        self.k = k
        self.shuffled_data = []
        self.data = data_set.tolist()
        
        for i in range(len(array)):
            self.selection = random.choice(self.data)
            self.shuffled_data.append(self.selection)            
            self.data.remove(self.selection)  # Be wary of remove for larger data sets, Big(O) increases
        
        #print(self.shuffled_data)
        
    # The data set is an array where there are 4 independent variables and one dependent variable.
    # The independent variables are put together into a list and acts as 'single' variable.
    # A fold in this case is a grouping of the independent variable list... a list of a list.
    # This function returns a list of all the folds created... a list of lists of lists
    def fold(self):
        self.fold_list = []
        self.fold_quantity = len(self.shuffled_data) / self.k
        
        # For populating folds
        n = 0
        m = 0
        
        for j in range(self.k):
            self.current_fold = []
            
            for i in range(int(self.fold_quantity)):
                self.current_fold.append(self.shuffled_data[int(self.fold_quantity*n + m)])
                m += 1
                
            self.fold_list.append(self.current_fold)
            n += 1
            m = 0
            
        return self.fold_list
