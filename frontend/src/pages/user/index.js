import {
  Card,
  Title,
  Pagination,
  CardList,
  Button,
  CheckboxGroup,
  Container,
  Main 
} from '../../components'
import cn from 'classnames'
import styles from './styles.module.css'
import { useRecipe } from '../../utils/index.js'
import { useEffect, useState, useContext } from 'react'
import api from '../../api'
import { useParams, useHistory } from 'react-router-dom'
import { UserContext } from '../../contexts'
import MetaTag from 'react-meta-tags'

const UserPage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipe,
    recipesCount,
    setRecipeCount,
    recipesPage,
    setRecipePage,
    tagsValue,
    setTagValue,
    handleTagChange,
    handleLike,
    handleAddToCart
  } = useRecipe()
  const { id } = useParams()
  const [ user, setUser ] = useState(null)
  const [ subscribed, setSubscribed ] = useState(false)
  const history = useHistory()
  const userContext = useContext(UserContext)

  const getRecipe = ({ page = 1, tags }) => {
    api
      .getRecipe({ page, author: id, tags })
        .then(res => {
          const { results, count } = res
          setRecipe(results)
          setRecipeCount(count)
        })
  }

  const getUser = () => {
    api.getUser({ id })
      .then(res => {
        setUser(res)
        setSubscribed(res.is_subscribed)
      })
      .catch(err => {
        history.push('/recipes')
      })
  }

  useEffect(_ => {
    if (!user) { return }
    getRecipe({ page: recipesPage, tags: tagsValue, author: user.id })
  }, [ recipesPage, tagsValue, user ])

  useEffect(_ => {
    getUser()
  }, [])

  useEffect(_ => {
    api.getTag()
      .then(tags => {
        setTagValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])


  return <Main>
    <Container className={styles.container}>
      <MetaTag>
        <title>{user ? `${user.first_name} ${user.last_name}` : 'Страница пользователя'}</title>
        <meta name="description" content={user ? `Продуктовый помощник - ${user.first_name} ${user.last_name}` : 'Продуктовый помощник - Страница пользователя'} />
        <meta property="og:title" content={user ? `${user.first_name} ${user.last_name}` : 'Страница пользователя'} />
      </MetaTag>
      <div className={styles.title}>
        <Title
          className={cn({
            [styles.titleText]: (userContext || {}).id !== (user || {}).id
          })}
          title={user ? `${user.first_name} ${user.last_name}` : ''}
        />
        <CheckboxGroup
          values={tagsValue}
          handleChange={value => {
            setRecipePage(1)
            handleTagChange(value)
          }}
        />
      </div>
      {(userContext || {}).id !== (user || {}).id && <Button
        className={styles.buttonSubscribe}
        clickHandler={_ => {
          const method = subscribed ? api.deleteSubscriptions.bind(api) : api.subscribe.bind(api) 
            method({
              author_id: id
            })
            .then(_ => {
              setSubscribed(!subscribed)
            })
        }}
      >
        {subscribed ? 'Отписаться от автора' : 'Подписаться на автора'}
      </Button>}
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

export default UserPage

