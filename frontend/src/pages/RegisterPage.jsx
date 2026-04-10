import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import axios from 'axios'

export function RegisterPage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const form = e.target


    const firstName = form.firstName.value.trim()
    const lastName = form.lastName.value.trim()
    const email = form.email.value.trim()
    const password = form.password.value

    const username = `${firstName}_${lastName}`.toLowerCase()

    try {
      await axios.post('http://localhost:8000/auth/register', {
        username,
        email,
        password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      navigate('/login')
    } catch (err) {
      console.log('Ошибка ответа:', err.response?.data)
      setError(err.response?.data?.detail || 'Ошибка регистрации')
    }
  }

  return (
    <div className="auth">
      <h1>Регистрация</h1>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}

      <form className="form" onSubmit={handleSubmit}>
        <div className="two-col">
          <label className="field">
            <span className="label">Имя</span>
            <input className="input" type="text" name="firstName" required />
          </label>

          <label className="field">
            <span className="label">Фамилия</span>
            <input className="input" type="text" name="lastName" required />
          </label>
        </div>

        <label className="field">
          <span className="label">Email</span>
          <input className="input" type="email" name="email" required />
        </label>

        <label className="field">
          <span className="label">Пароль</span>
          <input
            className="input"
            type="password"
            name="password"
            required
            maxLength={20}
          />
        </label>

        <button className="btn btn--secondary" type="submit">
          Зарегистрироваться
        </button>

        <div className="auth-footer">
          <span className="muted">Уже есть аккаунт? </span>
          <Link to="/login" className="link">
            Войти
          </Link>
        </div>
      </form>
    </div>
  )
}
