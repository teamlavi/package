import axios from "axios"

const URL_PREFIX = process.env.NODE_ENV === "development" ? "http://localhost:8080" : ""

export default class Service {

    static async getCds() {
        return axios.get(`${URL_PREFIX}/api/v1/cds`)
    }

    static async uploadCds(cds) {
        return axios.post(`${URL_PREFIX}/api/v1/cds`, cds)
    }

    static async getOriginalCds() {
        return axios.get(`${URL_PREFIX}/api/v1/cds/original`)
    }

    static async getVersions(repo, pkg) {
        return axios.get(`${URL_PREFIX}/api/v1/repositories/${repo}/versions`, {params: { name: pkg }})
    }

    static async runInstall(cmd, changes) {
        return axios.post(`${URL_PREFIX}/api/v1/install/${cmd}`, changes)
    }

    static async getStdout(id) {
        return axios.get(`${URL_PREFIX}/api/v1/dispatch/stdout`, { params: { id } })
    }

    static async getStatus(id) {
        return axios.get(`${URL_PREFIX}/api/v1/dispatch/status`, { params: { id } })
    }

}