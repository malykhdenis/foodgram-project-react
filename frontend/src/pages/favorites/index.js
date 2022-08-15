import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import styles from './styles.module.css'
import { useRecipe } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTag from 'react-meta-tags'

const Favorite = ({ updateOrders }) => {
  const {
    recipes,
    setRecipe,
    recipesCount,
    setRecipeCount,
    recipesPage,
    setRecipePage,
    tagsValue,
    handleTagChange,
    setTagValue,
    handleLike,
    handleAddToCart
  } = useRecipe()
  
  const getRecipe = ({ page = 1, tags }) => {
    api
      .getRecipe({ page, is_favorited: Number(true), tags })
      .then(res => {
        const { results, count } = res
        setRecipe(results)
        setRecipeCount(count)
      })
  }

  useEffect(_ => {
    getRecipe({ page: recipesPage, tags: tagsValue })
  }, [recipesPage, tagsValue])

  useEffect(_ => {
    api.getTag()
      .then(tags => {
        setTagValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])


  return <Main>
    <Container>
      <MetaTag>
        <title>Избранное</title>
        <meta name="description" content="Продуктовый помощник - Избранное" />
        <meta property="og:title" content="Избранное" />
      </MetaTag>
      <div className={styles.title}>
        <Title title='Избранное' />
        <CheckboxGroup
          values={tagsValue}
          handleChange={value => {
            setRecipePage(1)
            handleTagChange(value)
          }}
        />
      </div>
      <CardList>
        {recipes.map(card => <Card
          {...card}
          key={card.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>
      <Pagination
        count={recipesCount}
        limit={6}
        page={recipesPage}
        onPageChange={page => setRecipePage(page)}
      />
    </Container>
  </Main>
}

export default Favorite

