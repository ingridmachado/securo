import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/contexts/auth-context'
import { setup } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { ShellLogo } from '@/components/shell-logo'

export default function LoginPage() {
  const { t } = useTranslation()
  const { login, token } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (token) {
      navigate('/', { replace: true })
      return
    }
    setup.status().then(({ has_users }) => {
      if (!has_users) {
        navigate('/setup', { replace: true })
      }
    }).catch(() => {})
  }, [navigate, token])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)
    try {
      await login(email, password)
      navigate('/')
    } catch {
      setError(t('auth.invalidCredentials'))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-background via-background to-primary/5 px-4">
      <div className="flex items-center gap-3 mb-10">
        <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center">
          <ShellLogo size={24} className="text-primary" />
        </div>
        <span className="text-2xl font-bold tracking-tight text-foreground">{t('app.name')}</span>
      </div>
      <Card className="w-full max-w-[400px] shadow-lg border-border/60">
        <form onSubmit={handleSubmit}>
          <CardHeader className="text-center pb-2 pt-8 px-8">
            <CardTitle className="text-2xl font-bold tracking-tight">{t('auth.login')}</CardTitle>
            <CardDescription className="text-[13px] mt-1">{t('auth.loginDescription')}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 px-8 pt-4">
            {error && (
              <div className="p-3 text-sm text-destructive bg-destructive/10 rounded-lg">
                {error}
              </div>
            )}
            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-[13px] font-medium">{t('auth.email')}</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-11 rounded-lg text-sm"
                placeholder="you@example.com"
                required
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="password" className="text-[13px] font-medium">{t('auth.password')}</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-11 rounded-lg text-sm"
                required
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4 px-8 pb-8 pt-2">
            <Button type="submit" className="w-full h-11 rounded-lg text-sm font-semibold" disabled={isLoading}>
              {isLoading ? t('common.loading') : t('auth.login')}
            </Button>
            <p className="text-[13px] text-muted-foreground">
              {t('auth.noAccount')}{' '}
              <Link to="/register" className="text-primary font-medium hover:underline">
                {t('auth.register')}
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
