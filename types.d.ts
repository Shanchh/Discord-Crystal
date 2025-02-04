export interface Detail {
    _id: string,
    discord_id: string,
    discord_name: string,
    avatar: string,
    createAt: number,
    amount: number,
    quantity: number,
    payment: string,
}

export interface DetailModify {
    _id: string;
    name: string;
    createTime: string;
    payment: string;
    quantity: string;
    amount: string;
}

export interface UserData {
    _id: string,
    avatar: string,
    discord_id: string,
    discord_name: string,
    createAt: number,
    is_active: boolean,
    total_amount: number,
    total_quantity: number,
}