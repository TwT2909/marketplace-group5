import { NavLink, Outlet } from 'react-router-dom'

export function Layout() {
  return (
    <>
      <header className="header">
        <div className="container header__row">
          <NavLink to="/login" className="logo">
            Market
          </NavLink>

          <nav className="menu">
            <NavLink to="/login" className="menu__link">
              Вход
            </NavLink>
            <NavLink to="/register" className="menu__link">
              Регистрация
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="container main">
        <Outlet />
      </main>
    </>
  )
}

