import login from './login.js'
import project from './project.js'

function merge (...sources) {
  return Object.assign({}, ...sources)
}
const api = merge(
  {login: login},
  {project: project}
)
export default api
