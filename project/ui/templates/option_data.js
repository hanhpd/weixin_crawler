//Cumulative Total Posts
document.getElementById('total_posts_num').innerHTML = '{{ data.account_name }}'+'{{ data.posts_info }}'


// Release time of historical main articles / views / likes / comments / comments
echarts.init(document.getElementById('all_mian_date_read')).setOption({{ data.all_mian_date_read }})

// Primary and secondary article statistics
echarts.init(document.getElementById('all_statistic')).setOption({{ data.all_statistic }})

// Count the number of articles published by different main / secondary / hour / week separately
echarts.init(document.getElementById('dir_posts_num_related_mov')).setOption({{ data.dir_posts_num_related.mov }})
echarts.init(document.getElementById('dir_posts_num_related_hour')).setOption({{ data.dir_posts_num_related.hour }})
echarts.init(document.getElementById('dir_posts_num_related_week')).setOption({{ data.dir_posts_num_related.week }})

//The relationship between reading volume and likes / last reading volume
echarts.init(document.getElementById('read_vs_like')).setOption({{ data.read_vs_factors.like }})
echarts.init(document.getElementById('read_vs_pre_read')).setOption({{ data.read_vs_factors.pre_read }})

// Explore the best tweet hours Tweet week Number of titles Number of illustrations Number of videos
echarts.init(document.getElementById('read_vs_hour')).setOption({{ data.find_best_factors.hour }})
echarts.init(document.getElementById('read_vs_week')).setOption({{ data.find_best_factors.week }})
echarts.init(document.getElementById('read_vs_title')).setOption({{ data.find_best_factors.title }})
echarts.init(document.getElementById('read_vs_pic')).setOption({{ data.find_best_factors.pic }})
echarts.init(document.getElementById('read_vs_video')).setOption({{ data.find_best_factors.video }})


{% macro table_list(table_data) -%}
`
<table class="w3-table w3-striped w3-white">
    <thead>
        <tr>
            <th scope="col">Serial number</th>
            <th scope="col">Reading</th>
            <th scope="col">Likes</th>
            <th scope="col">title</th>
            <th scope="col">Post date</th>
            <th scope="col">{{ table_data.attribute }}</th>
        </tr>
    </thead>
    <tbody>
        {% for data in table_data.data %}
        <tr>
            <td>{{ data.id }}</td>
            <td>{{ data.read }}</td>
            <td>{{ data.like }}</td>
            <td><a class='text-body' href={{ data.url }} target="_blank">{{ data.title_cnt }}</a></td>
            <td>{{ data.date }}</td>
            <td>{{ data.attribute }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
`
{%- endmacro %}
// Table 9 Except 100001 Read the top 10 articles
document.getElementById('particular_most_read_10_except_100001').innerHTML = {{ table_list(data.table.particular_most_read_10_except_100001) }}
// Table 10 The 10 most read and non-zero articles
document.getElementById('particular_least_read_10_except_0').innerHTML = {{ table_list(data.table.particular_least_read_10_except_0) }}
// Table 11 The 10 articles with the highest depth index
document.getElementById('particular_most_deep_10').innerHTML = {{ table_list(data.table.particular_most_deep_10) }}
// Table 12 The 10 articles with the lowest depth index
document.getElementById('particular_least_deep_10').innerHTML = {{ table_list(data.table.particular_least_deep_10) }}
// Table 13 The 10 articles with the lowest drop index
document.getElementById('particular_least_fall_10').innerHTML = {{ table_list(data.table.particular_least_fall_10) }}
// Table 14 All 100001 Articles
document.getElementById('particular_all_10001').innerHTML = {{ table_list(data.table.particular_all_10001) }}
