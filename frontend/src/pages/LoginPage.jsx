import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { authAPI } from '../api/auth.js'

export function LoginPage() {
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const formData = new FormData(e.target)

    try {
      const { data } = await authAPI.login({
        username: formData.get('username'),
        password: formData.get('password'),
      })

      localStorage.setItem('token', data.access_token)
      navigate('/') // Добавить переход на главную страницу после успешного входа
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка входа')
    }
  }

  return (
    <div className="auth">
      <h1>Вход</h1>

      {error && <div className="error">{error}</div>}

      <form className="form" onSubmit={handleSubmit}>
        <label className="field">
          <span className="label">Имя пользователя</span>
          <input
            className="input"
            type="text"
            name="username"
            placeholder="username"
            required
          />
        </label>

        <label className="field">
          <span className="label">Пароль</span>
          <input className="input" type="password" name="password" required />
        </label>

        <button className="btn btn--secondary" type="submit">
          Войти
        </button>

        <div className="auth-footer">
          <span className="muted">Нет аккаунта? </span>
          <Link to="/register" className="link">
            Регистрация
          </Link>
        </div>
      </form>
    </div>
  )
}
