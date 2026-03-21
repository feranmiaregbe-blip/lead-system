while True:
 name=input("Customer Name:")
 location=input("Preferred location:")
 budget=input("Budget:")
 Lead=name+"|"+location+"|"+budget
 file=open("leads.txt","a")
 file.write(Lead+"\n")
 file.close()
 print("Lead saved succesfully.")
 another=input("Add another lead?(yes/no):")
 if another.lower()=="no":
    print("Program closed.")
    break