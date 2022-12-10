from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app, conn

@app.route('/post_recipe')
def post_recipe():
    return render_template('create_recipe.html')


@app.route('/create_recipe')
def create_recipe():
    username = session['username']
    # cursor = conn.cursor();
    # query = 'SELECT * FROM Recipe where postedBy = %s'
    # cursor.execute(query, username)
    # recipes = cursor.fetchall()
    # cursor.close()
    return render_template('create_recipe.html')

#Authenticates the register
@app.route('/createRecipe', methods=['GET', 'POST'])
def createRecipe():
    username = session['username']
    #grabs information from the forms
    title = request.form['title']
    numServings = request.form['numServings']
    numDietRestr = request.form['numDietaryRestrictions']
    recipeTags = request.form['recipeTags']
    restrictions_detail_map = dict()
    for i in range(0, int(numDietRestr)):
        curr_rst = "name_rst" + str(i);
        curr_desc = "desc_rst" + str(i);
        restrictions_detail_map[i] = [request.form[curr_rst], request.form[curr_desc]]

    numOfIng = request.form['numIngredients']
    ingr_detail_map = dict()
    for i in range(0, int(numOfIng)):
        # ingr_detail_map would have entries like:
        #   { 1 : ['strawberry', 'gram', 10 ],
        #     2 : ['banana', 'gram', 10 ], }
        curr_ing_name = "name_ing" + str(i);
        curr_unit_name = "unitName_ing" + str(i);
        curr_amount = "amount_ing" + str(i);
        curr_purchase_link = "purchase_link_ing" + str(i);
        ingr_detail_map[i] = [request.form[curr_ing_name], request.form[curr_unit_name], 
        request.form[curr_amount], request.form[curr_purchase_link]]
    
    cursor = conn.cursor()
    query = 'SELECT * FROM Recipe WHERE title = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    error = None
    if(data):
        # if recipe with same title exists in DB, stop them from creating the recipe.
        error = "This recipe already exists"
        return render_template('create_recipe.html', error = error)
    else:
        query = 'SELECT'
        ins = 'INSERT INTO Recipe (title, numServings, postedBy) VALUES (%s, %s, %s)'
        cursor.execute(ins, (title, int(numServings), username))
        conn.commit()
        currRecipeID = cursor.lastrowid #Fetch the most recently added ID
        
        ###### RecipeTag table ########
        # example input for recipe tags: "French, Italian, Dessert"
        splittedArr = recipeTags.split(",")
        for i in splittedArr:
            ins = 'INSERT INTO RecipeTag (recipeID, tagText) VALUES (%s, %s)'
            cursor.execute(ins, (currRecipeID, i))
            conn.commit()

        ######## Ingredient Table #########
        # check if any of these ingredients are already found in the Ingredient DB.
        for key, val in ingr_detail_map.items():
            # ingr_detail_map looks like: key is 0 and value is ['strawberry', 'Gram', '3']
            # For each ingredient:
            # 1. Insert a new entry into Ingredient table if not already in DB.
            
            ######### Ingredient Table #########
            query = 'SELECT * FROM Ingredient WHERE iName = %s'
            cursor.execute(query, (val[0]))
            data = cursor.fetchone()
            ingredientName = val[0]
            if not data:
                ins = 'INSERT INTO Ingredient (iName, purchaseLink) VALUES (%s, %s)'
                cursor.execute(ins, (ingredientName, val[3]))

            ######### Unit Table #########
            query = 'SELECT * FROM Unit WHERE unitName = %s'
            cursor.execute(query, (val[1]))
            data = cursor.fetchone()
            unitName = val[1]
            if not data:
                ins = 'INSERT INTO Unit (unitName) VALUES (%s)'
                cursor.execute(ins, (unitName))

            ######### RecipeIngredient Table #########
            # 2. Add an entry into RecipeIngredient Table
            ins = 'INSERT INTO RecipeIngredient (recipeID, iName, unitName, amount) VALUES (%s, %s, %s, %s)'
            cursor.execute(ins, (currRecipeID, ingredientName, val[1],int(val[2])))
            conn.commit()


        ###### Restrictions table ########
        # TODO: FIX!!!!!!
        for key, val in restrictions_detail_map.items():
            print(key, val)
            query = 'SELECT * FROM Ingredient WHERE iName = %s'
            cursor.execute(query, val[0])
            data = cursor.fetchone()
            if data:
                # Only add an entry to Restrictions table ONLY IF ingredient exists. 
                ins = 'INSERT INTO Restrictions (iName, restrictionDesc) VALUES (%s, %s)'
                cursor.execute(ins, (val[0], val[1])) # TODO: pass in the actual value for restrictionDesc!!!
                conn.commit()


        cursor.close()
        return render_template('dashboard.html')
    

# @app.route('/recipe-info')
# def create_recipe():
#     username = session['username']
#     # cursor = conn.cursor();
#     # query = 'SELECT * FROM Recipe where postedBy = %s'
#     # cursor.execute(query, username)
#     # recipes = cursor.fetchall()
#     # cursor.close()
#     return render_template('create_recipe.html')
