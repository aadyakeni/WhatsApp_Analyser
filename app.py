import streamlit as st
import preprocessing,helper
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

st.set_page_config(layout="centered", initial_sidebar_state="expanded")

font_path = 'C:\\Users\\Aadya\\Downloads\\Noto_Color_Emoji\\NotoColorEmoji-Regular.ttf'
emoji_font = fm.FontProperties(fname=font_path)

st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)

    df = preprocessing.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    with open("assets/style.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)

        #Stats Area
        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns([1.2,1,1,1])

        with col1:
            st.header("Total Messages")
            st.title(num_messages)  

        with col2:
            st.header("Total Words")
            st.title(words)  
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = '#66ff00')
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#212837')
        plt.xticks(rotation = 'vertical', color = 'white')
        plt.yticks(color = 'white')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color = '#ffff4d')
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#212837')
        plt.xticks(rotation = 'vertical',color = 'white')
        plt.yticks(color = 'white')
        st.pyplot(fig)

        #Activity Map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values, color='purple')
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            plt.xticks(rotation = 'vertical' , color='white')
            plt.yticks(color = 'white')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values, color = 'orange')
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            plt.xticks(rotation = 'vertical', color = 'white')
            plt.yticks(color = 'white')
            st.pyplot(fig)

        #HeatMap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heat_map(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        fig.patch.set_facecolor('#0E1117')
        plt.xticks(color = 'white')
        plt.yticks(color = 'white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        st.pyplot(fig)


        #Finding Busiest users
        if selected_user == 'Overall':

            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)

            fig,ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values , color = 'red')
                plt.xticks(rotation='vertical')
                fig.patch.set_facecolor('#0E1117')
                ax.set_facecolor('#0E1117')
                plt.xticks(color = 'white')
                plt.yticks(color = 'white')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)

        #Creating WordCloud
        st.title("WordCloud")
        df_wc = helper.create_worldcloud(selected_user,df)

        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        plt.xticks(color = 'white')
        plt.yticks(color = 'white')
        st.pyplot(fig)

        #Most common words
        most_common_df = helper.most_common_words(selected_user,df)
        
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1] , color = '#9854cb')
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        plt.xticks(color = 'white')
        plt.yticks(color = 'white')

        st.title("Most Common Words")
        st.pyplot(fig)

        #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)

        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:

            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct= "%0.2f")
            fig.patch.set_facecolor('#0E1117')
            st.pyplot(fig)



   