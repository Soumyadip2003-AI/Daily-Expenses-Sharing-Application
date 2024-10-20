import csv

def generate_balance_sheet():
  
    file_path = 'balance_sheet.csv'
    with open(file_path, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Total Expense', 'Owed Amount'])
        
        
        writer.writerow(['John Doe', 3000, 1000])
    
    return file_path
