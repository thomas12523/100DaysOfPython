import spec

def pago():
    quaters= int(input("how many quarters?:"))
    dimes= int(input("how many dimes?:"))
    nickles= int(input("how many nickles?:"))
    pennies= int(input("how many pennies?:"))
    return quaters*0.25+dimes*0.10+nickles*0.05+pennies*0.01

def contabilizar(pedido):
    spec.resources["water"]-=spec.MENU[pedido]["ingredients"]['water']
    spec.resources["milk"]-=spec.MENU[pedido]["ingredients"]['milk']
    spec.resources["coffee"]-=spec.MENU[pedido]["ingredients"]['coffee']
    spec.profit+=spec.MENU[pedido]['cost']

def verificacion_stock(pedido):
    if spec.resources["water"]<spec.MENU[pedido]["ingredients"]['water']:
            print("Sorry there is not enough water.")      
    elif spec.resources["milk"]<spec.MENU[pedido]["ingredients"]['milk']:
            print("Sorry there is not enough milk.")        
    elif spec.resources["coffee"]<spec.MENU[pedido]["ingredients"]['coffee']:
            print("Sorry there is not enough coffee.")
    else:
         return "Todo ok"
            

while True:
    pedido=input("What would you like? (espresso/latte/cappuccino): ")
    if pedido=="report":
        print("Water: " +str(spec.resources['water']) + "ml" + "\n" + "Milk: "+str(spec.resources['milk']) + "ml" + "\n" + str(spec.resources['coffee']) + "g" + "\n" + "money: $" + str(spec.profit))

    elif pedido=="off":
        break
    elif pedido=="espresso":
        if spec.resources["water"]<spec.MENU[pedido]["ingredients"]['water']:
            print("Sorry there is not enough water.")
        elif spec.resources["coffee"]<spec.MENU[pedido]["ingredients"]['coffee']:
            print("Sorry there is not enough coffee.")
        else:
            print("")
            print("Please insert coins.")
            count=pago()
            if count<spec.MENU[pedido]['cost']:
                print("Sorry that's enough money. Money refunded")
            else:
                spec.resources["water"]-=spec.MENU[pedido]["ingredients"]['water']
                spec.resources["coffee"]-=spec.MENU[pedido]["ingredients"]['coffee']
                spec.profit+=spec.MENU[pedido]['cost']
                print(f"Here is ${round(-spec.MENU[pedido]['cost']+count,2)} in change.")
                print(f"Here is your {pedido}. Enjoy! ")
    elif pedido=="latte":
        if verificacion_stock(pedido) =="Todo ok":
            print("")
            print("Please insert coins.")
            count=pago()
            if count<spec.MENU[pedido]['cost']:
                print("Sorry that's enough money. Money refunded")
            else:
                contabilizar(pedido)
                print(f"Here is ${round(-spec.MENU[pedido]['cost']+count,2)} in change.")
                print(f"Here is your {pedido}. Enjoy! ")
    elif pedido=="cappuccino":
        if verificacion_stock(pedido) =="Todo ok":
            print("")
            print("Please insert coins.")
            count=pago()
            if count<spec.MENU[pedido]['cost']:
                print("Sorry that's enough money. Money refunded")
            else:
                contabilizar(pedido)
                print(f"Here is ${round(-spec.MENU[pedido]['cost']+count,2)} in change.")
                print(f"Here is your {pedido}. Enjoy! ")