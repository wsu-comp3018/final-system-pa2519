import Cookie from 'js-cookie';
export const signoutAndRedirect = (axiosInstance) => {
if(axiosInstance)
{
axiosInstance.post('signin')
.finally(() => {
clearSignedInVariables()
redirectToSignin()
})
}
else
{
clearSignedInVariables()
redirectToSignin()
}
}
export const redirectToSignin = () => {
window.location.href = '/signin'
}
export const clearSignedInVariables = () => {
Cookie.remove('root_api_token')
Cookie.remove('api_token')
localStorage.removeItem('user_id')
localStorage.removeItem('user')
localStorage.setItem('redirect', window.location.href)
}
export const isAuthenticated = () => {
return Cookie.get('api_token') != null
}
export const redirectAfterSignin = (token) => {
console.log('redirect', token)
Cookie.set('root_api_token', token)
Cookie.set('api_token', token)
let redirected = localStorage.getItem('redirect')
if(redirected)
{
localStorage.removeItem('redirect')
window.location.href = redirected
}
else
{
window.location.href = '/'
}
}