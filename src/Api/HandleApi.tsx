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

export const modify_detail = async (values: any) => {
    try {
        const res = await axios.post("/monthly/modify_detail", { values });
        return res.data;
    }
    catch (err) {
        throw err;
    }
}

export const delete_detail = async (id: string) => {
    try {
        const res = await axios.post("/monthly/delete_detail", { id });
        return res.data;
    }
    catch (err) {
        throw err;
    }
}