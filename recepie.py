import streamlit as st
import google.generativeai as genai
import json

def generate_recipe(food, profession, dietary_preference, cuisine_type, meal_type, skill_level, cooking_time):
    """Generates a recipe based on given parameters.

    Args:
        food: The type of food.
        profession: The target user's profession.
        dietary_preference: Dietary restrictions or preferences.
        cuisine_type: The type of cuisine.
        meal_type: Type of meal (breakfast, lunch, etc.).
        skill_level: Cooking skill level required.
        cooking_time: Approximate cooking time.

    Returns:
        A dictionary containing the recipe, or None if an error occurs.
    """

    try:
        # Configure API key
        genai.configure(api_key="AIzaSyAXzDLQWJevEw3Z8KVwyD3PxaGTY_OtxVM")

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert chef. Create delicious recipes tailored to the user's needs, including food type, profession, dietary preferences, cuisine, meal type, skill level, and cooking time.",
        )

        # Construct the prompt
        prompt = (
            f"Create a {meal_type} recipe for a {profession} that features {food}. "
            f"Ensure it meets the {dietary_preference} dietary preference and has elements of {cuisine_type} cuisine. "
            f"The recipe should be suitable for a {skill_level} cook and take around {cooking_time} to prepare. "
            "Include a clear list of ingredients with quantities and detailed instructions."
        )

        # Generate the recipe
        response = model.generate_content(prompt)
        recipe_text = response.text

        # Basic recipe formatting (you can enhance this)
        recipe_dict = {"ingredients": [], "instructions": []}
        current_section = "ingredients"
        for line in recipe_text.split("\n"):
            if line.startswith("Ingredients:"):
                current_section = "ingredients"
            elif line.startswith("Instructions:"):
                current_section = "instructions"
            else:
                recipe_dict[current_section].append(line)

        return recipe_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Streamlit UI
st.title("AI Recipe Generator")

food = st.text_input("Enter the main food ingredient:")
profession = st.text_input("Enter the target profession:")
dietary_preference = st.text_input("Enter dietary preferences (e.g., vegan, gluten-free):")
cuisine_type = st.text_input("Enter the type of cuisine:")
meal_type = st.text_input("Enter the type of meal (e.g., breakfast, lunch):")
skill_level = st.selectbox("Select the skill level required:", ["beginner", "intermediate", "advanced"])
cooking_time = st.text_input("Enter the approximate cooking time:")
st.snow()
if st.button("Generate Recipe"):
    recipe = generate_recipe(food, profession, dietary_preference, cuisine_type, meal_type, skill_level, cooking_time)

    if recipe:
        st.header("Ingredients")
        for ingredient in recipe["ingredients"]:
            st.write("- " + ingredient)
        st.header("Instructions")
        for step in recipe["instructions"]:
            st.write("- " + step)
    else:
        st.error("Failed to generate recipe.")
