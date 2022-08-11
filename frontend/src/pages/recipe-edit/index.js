import { Container, IngredientSearch, FileInput, Input, Title, CheckboxGroup, Main, Form, Button, Checkbox, Textarea } from '../../components'
import styles from './styles.module.css'
import api from '../../api'
import { useEffect, useState } from 'react'
import { useTag } from '../../utils'
import { useParams, useHistory } from 'react-router-dom'
import MetaTag from 'react-meta-tags'

const RecipeEdit = ({ onItemDelete }) => {
  const { value, handleChange, setValue } = useTag()
  const [ recipeName, setRecipeName ] = useState('')

  const [ ingredientValue, setIngredientValue ] = useState({
    name: '',
    id: null,
    amount: '',
    measurement_unit: ''
  })

  const [ recipeIngredient, setRecipeIngredient ] = useState([])
  const [ recipeText, setRecipeText ] = useState('')
  const [ recipeTime, setRecipeTime ] = useState(0)
  const [ recipeFile, setRecipeFile ] = useState(null)
  const [
    recipeFileWasManuallyChanged,
    setRecipeFileWasManuallyChanged
  ] = useState(false)

  const [ ingredients, setIngredient ] = useState([])
  const [ showIngredient, setShowIngredient ] = useState(false)
  const [ loading, setLoading ] = useState(true)
  const history = useHistory()

  useEffect(_ => {
    if (ingredientValue.name === '') {
      return setIngredient([])
    }
    api
      .getIngredient({ name: ingredientValue.name })
      .then(ingredients => {
        setIngredient(ingredients)
      })
  }, [ingredientValue.name])

  useEffect(_ => {
    api.getTag()
      .then(tags => {
        setValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])

  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getRecipe ({
      recipe_id: id
    }).then(res => {
      const {
        image,
        tags,
        cooking_time,
        name,
        ingredients,
        text
      } = res
      setRecipeText(text)
      setRecipeName(name)
      setRecipeTime(cooking_time)
      setRecipeFile(image)
      setRecipeIngredient(ingredients)


      const tagsValueUpdated = value.map(item => {
        item.value = Boolean(tags.find(tag => tag.id === item.id))
        return item
      })
      setValue(tagsValueUpdated)
      setLoading(false)
    })
    .catch(err => {
      history.push('/recipes')
    })
  }, [value])

  const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
    setIngredientValue({
      ...ingredientValue,
      id,
      name,
      measurement_unit
    })
  }

  const checkIfDisabled = () => {
    return recipeText === '' ||
    recipeName === '' ||
    recipeIngredient.length === 0 ||
    value.filter(item => item.value).length === 0 ||
    recipeTime === '' ||
    recipeFile === '' ||
    recipeFile === null
  }

  return <Main>
    <Container>
      <MetaTag>
        <title>Редактирование рецепта</title>
        <meta name="description" content="Продуктовый помощник - Редактирование рецепта" />
        <meta property="og:title" content="Редактирование рецепта" />
      </MetaTag>
      <Title title='Редактирование рецепта' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          const data = {
            text: recipeText,
            name: recipeName,
            ingredients: recipeIngredient.map(item => ({
              id: item.id,
              amount: item.amount
            })),
            tags: value.filter(item => item.value).map(item => item.id),
            cooking_time: recipeTime,
            image: recipeFile,
            recipe_id: id
          }
          api
            .updateRecipe(data, recipeFileWasManuallyChanged)
            .then(res => {
              history.push(`/recipes/${id}`)
            })
            .catch(err => {
              const { non_field_errors, ingredients, cooking_time } = err
              console.log({  ingredients })
              if (non_field_errors) {
                return alert(non_field_errors.join(', '))
              }
              if (ingredients) {
                return alert(`Ингредиенты: ${ingredients.filter(item => Object.keys(item).length).map(item => {
                  const error = item[Object.keys(item)[0]]
                  return error && error.join(' ,')
                })[0]}`)
              }
              if (cooking_time) {
                return alert(`Время готовки: ${cooking_time[0]}`)
              }
              const errors = Object.values(err)
              if (errors) {
                alert(errors.join(', '))
              }
            })
        }}
      >
        <Input
          label='Название рецепта'
          onChange={e => {
            const value = e.target.value
            setRecipeName(value)
          }}
          value={recipeName}
        />
        <CheckboxGroup
          label='Теги'
          values={value}
          className={styles.checkboxGroup}
          labelClassName={styles.checkboxGroupLabel}
          tagsClassName={styles.checkboxGroupTag}
          checkboxClassName={styles.checkboxGroupItem}
          handleChange={handleChange}
        />
        <div className={styles.ingredients}>
          <div className={styles.ingredientsInputs}>
            <Input
              label='Ингредиенты'
              className={styles.ingredientsNameInput}
              inputClassName={styles.ingredientsInput}
              labelClassName={styles.ingredientsLabel}
              onChange={e => {
                const value = e.target.value
                setIngredientValue({
                  ...ingredientValue,
                  name: value
                })
              }}
              onFocus={_ => {
                setShowIngredient(true)
              }}
              value={ingredientValue.name}
            />
            <div className={styles.ingredientsAmountInputContainer}>
              <Input
                className={styles.ingredientsAmountInput}
                inputClassName={styles.ingredientsAmountValue}
                onChange={e => {
                  const value = e.target.value
                  setIngredientValue({
                    ...ingredientValue,
                    amount: value
                  })
                }}
                value={ingredientValue.amount}
              />
              {ingredientValue.measurement_unit !== '' && <div className={styles.measurementUnit}>{ingredientValue.measurement_unit}</div>}
            </div>
            {showIngredient && ingredients.length > 0 && <IngredientSearch
              ingredients={ingredients}
              onClick={({ id, name, measurement_unit }) => {
                handleIngredientAutofill({ id, name, measurement_unit })
                setIngredient([])
                setShowIngredient(false)
              }}
            />}
          </div>
          <div className={styles.ingredientsAdded}>
            {recipeIngredient.map(item => {
              return <div
                className={styles.ingredientsAddedItem}
              >
                <span className={styles.ingredientsAddedItemTitle}>{item.name}</span> <span>-</span> <span>{item.amount}{item.measurement_unit}</span> <span
                  className={styles.ingredientsAddedItemRemove}
                  onClick={_ => {
                    const recipeIngredientUpdated = recipeIngredient.filter(ingredient => {
                      return ingredient.id !== item.id
                    })
                    setRecipeIngredient(recipeIngredientUpdated)
                  }}
                >Удалить</span>
              </div>
            })}
          </div>
          <div
            className={styles.ingredientAdd}
            onClick={_ => {
              if (ingredientValue.amount === '' || ingredientValue.name === '') { return }
              setRecipeIngredient([...recipeIngredient, ingredientValue])
              setIngredientValue({
                name: '',
                id: null,
                amount: '',
                measurement_unit: ''
              })
            }}
          >
            Добавить ингредиент
          </div>
        </div>
        <div className={styles.cookingTime}>
          <Input
            label='Время приготовления'
            className={styles.ingredientsTimeInput}
            labelClassName={styles.cookingTimeLabel}
            inputClassName={styles.ingredientsTimeValue}
            onChange={e => {
              const value = e.target.value
              setRecipeTime(value)
            }}
            value={recipeTime}
          />
          <div className={styles.cookingTimeUnit}>мин.</div>
        </div>
        <Textarea
          label='Описание рецепта'
          onChange={e => {
            const value = e.target.value
            setRecipeText(value)
          }}
          value={recipeText}
        />
        <FileInput
          onChange={file => {
            setRecipeFileWasManuallyChanged(true)
            setRecipeFile(file)
          }}
          className={styles.fileInput}
          label='Загрузить фото'
          file={recipeFile}
        />
        <div className={styles.actions}>
          <Button
            modifier='style_dark-blue'
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Редактировать рецепт
          </Button>
          <div
            className={styles.deleteRecipe}
            onClick={_ => {
              api.deleteRecipe({ recipe_id: id })
                .then(res => {
                  onItemDelete && onItemDelete()
                  history.push('/recipes')
                })
            }}
          >
            Удалить
          </div>
        </div>
      </Form>
    </Container>
  </Main>
}

export default RecipeEdit
