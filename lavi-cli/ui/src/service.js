import axios from "axios"

const URL_PREFIX = process.env.NODE_ENV === "development" ? "http://localhost:8080" : ""

export default class Service {

    static async getCds() {
        return axios.get(`${URL_PREFIX}/api/v1/cds`)
    }

    static async getOriginalCds() {
        return axios.get(`${URL_PREFIX}/api/v1/cds/original`)
    }

    static async getVersions(repo, pkg) {
        return axios.get(`${URL_PREFIX}/api/v1/repositories/${repo}/packages/${pkg}/versions`)
    }

    static async runInstall(repo, changes) {
        return axios.post(`${URL_PREFIX}/api/v1/repositories/${repo}/install`, changes)
    }

    static async getStdout(id) {
        return axios.get(`${URL_PREFIX}/api/v1/dispatch/stdout`, { params: { id } })
    }

    static async getStatus(id) {
        return axios.get(`${URL_PREFIX}/api/v1/dispatch/status`, { params: { id } })
    }

}