import React, { useState } from "react";
import { useTag } from './index.js'
import api from '../api'

export default function useRecipe () {
  const [ recipes, setRecipe ] = useState([])
  const [ recipesCount, setRecipeCount ] = useState(0)
  const [ recipesPage, setRecipePage ] = useState(1)
  const { value: tagsValue, handleChange: handleTagChange, setValue: setTagValue } = useTag()

  const handleLike = ({ id, toLike = true }) => {
    const method = toLike ? api.addToFavorite.bind(api) : api.removeFromFavorite.bind(api)
    method({ id }).then(res => {
      const recipesUpdated = recipes.map(recipe => {
        if (recipe.id === id) {
          recipe.is_favorited = toLike
        }
        return recipe
      })
      setRecipe(recipesUpdated)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  const handleAddToCart = ({ id, toAdd = true, callback }) => {
    const method = toAdd ? api.addToOrders.bind(api) : api.removeFromOrders.bind(api)
    method({ id }).then(res => {
      const recipesUpdated = recipes.map(recipe => {
        if (recipe.id === id) {
          recipe.is_in_shopping_cart = toAdd
        }
        return recipe
      })
      setRecipe(recipesUpdated)
      callback && callback(toAdd)
    })
    .catch(err => {
      const { errors } = err
      if (errors) {
        alert(errors)
      }
    })
  }

  return {
    recipes,
    setRecipe,
    recipesCount,
    setRecipeCount,
    recipesPage,
    setRecipePage,
    tagsValue,
    handleLike,
    handleAddToCart,
    handleTagChange,
    setTagValue
  }
}
