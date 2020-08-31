const development = {
    // BASE_URL: 'http://127.0.0.1:5000'
    BASE_URL: 'https://cors-anywhere.herokuapp.com/http://ids.idostuff.today'
}

const production = {
    BASE_URL: 'http://ids.idostuff.today'
}

const config = process.env.NODE_ENV === "development" ? development : production

export default config