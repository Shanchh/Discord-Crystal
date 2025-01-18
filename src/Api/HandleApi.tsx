import axios from "axios";

export const get_all_detail_lists = async () => {
    try {
        const res = await axios.get("/monthly/get_all_detail_lists");
        return res.data.data;
    }
    catch (err) {
        throw err;
    }
}