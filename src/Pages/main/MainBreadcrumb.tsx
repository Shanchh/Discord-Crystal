import React from "react";
import { Breadcrumb } from "antd";
import { useLocation, Link } from "react-router-dom";

const breadcrumbNameMap: Record<string, string> = {
    "/": "首頁",
    "/dashboard": "儀錶板",
    "/user-manage": "用戶列表",
    "/detail-manage": "訂閱明細"
};

const MainBreadcrumb: React.FC = () => {
    const location = useLocation();

    const pathSnippets = location.pathname.split("/").filter((i) => i);
    const breadcrumbItems = [
        {
            title: <Link to="/">首頁</Link>,
            key: "home",
        },
        ...pathSnippets.map((_, index) => {
            const url = `/${pathSnippets.slice(0, index + 1).join("/")}`;
            const isLast = index === pathSnippets.length - 1;
            return {
                title: isLast ? breadcrumbNameMap[url] || url : <Link to={url}>{breadcrumbNameMap[url] || url}</Link>,
                key: url,
            };
        }),
    ];

    return <Breadcrumb style={{ margin: "12px 0" }} items={breadcrumbItems} />;
};

export default MainBreadcrumb;
