import { PurchaseList, Title, Container, Main, Button } from '../../components'
import styles from './styles.module.css'
import { useRecipe } from '../../utils/index.js'
import { useEffect, useState } from 'react'
import api from '../../api'
import MetaTag from 'react-meta-tags'

const Cart = ({ updateOrders, orders }) => {
  const {
    recipes,
    setRecipe,
    handleAddToCart
  } = useRecipe()
  
  const getRecipe = () => {
    api
      .getRecipe({
        page: 1,
        limit: 999,
        is_in_shopping_cart: Number(true)
      })
      .then(res => {
        const { results } = res
        setRecipe(results)
      })
  }

  useEffect(_ => {
    getRecipe()
  }, [])

  const downloadDocument = () => {
    api.downloadFile()
  }

  return <Main>
    <Container className={styles.container}>
      <MetaTag>
        <title>Список покупок</title>
        <meta name="description" content="Продуктовый помощник - Список покупок" />
        <meta property="og:title" content="Список покупок" />
      </MetaTag>
      <div className={styles.cart}>
        <Title title='Список покупок' />
        <PurchaseList
          orders={recipes}
          handleRemoveFromCart={handleAddToCart}
          updateOrders={updateOrders}
        />
        {orders > 0 && <Button
          modifier='style_dark-blue'
          clickHandler={downloadDocument}
        >Скачать список</Button>}
      </div>
    </Container>
  </Main>
}

export default Cart

