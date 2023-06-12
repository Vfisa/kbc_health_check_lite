import loggingfrom main_app import start_date, end_date, connfrom utils import utils#from utils import run_query, create_linkimport pandas as pdimport streamlit as stimport sqlsst.markdown("# Components and Configurations")JOB_FIELDS = 'j."kbc_component_id", j."kbc_component_configuration_id", j."job_time_credits_used", j."kbc_job_id", j."kbc_project_id"'        logging.debug(f'imported project from state ids {st.session_state["project_ids_str"]}')try:    sql_jobs = sqls.prepare_sql_jobs(JOB_FIELDS, start_date, end_date)                logging.debug(sql_jobs)    jobs_df = utils.run_query(sql_jobs, conn)          jobs_df2 = jobs_df.copy().loc[(jobs_df.kbc_configuration_is_deleted=='false') & (jobs_df.kbc_project_id.isin(st.session_state["selected_project_ids"])), :]    jobs_df2.drop(columns=["kbc_project_id"], inplace=True)    jobs_df2["job_time_credits_used"] = pd.to_numeric(jobs_df2["job_time_credits_used"])        most_common_components = jobs_df2.groupby("kbc_component_id").agg(job_count=('kbc_job_id','count'), time_credits_used=('job_time_credits_used','sum'))    most_common_components.sort_values(by="time_credits_used", ascending=False, inplace=True)            most_consuming_configs = jobs_df2.groupby('kbc_component_configuration_id').agg(time_credits_used=('job_time_credits_used','sum'),                                                                                    njobs=('job_time_credits_used','count'))    most_consuming_configs.reset_index(inplace=True)    most_consuming_configs["configuration"] = most_consuming_configs.kbc_component_configuration_id.apply(lambda x: x.split('_')[-1])    most_consuming_configs["kbc_component_id"] = most_consuming_configs.kbc_component_configuration_id.apply(lambda x: x.split('_')[-2])    most_consuming_configs["config_link"] = most_consuming_configs.kbc_component_configuration_id.apply(lambda x: utils.create_link(x, jobs_df))    most_consuming_configs.sort_values(by="time_credits_used", ascending=False, inplace=True)    col_components, col_configs = st.columns(2)    tab_components, tab_configurations = st.tabs(["Components", "Configurations"])    with tab_components:    #with col_components:        st.subheader("Most Consuming Components")        #st.dataframe(most_common_components)        st.write(most_common_components.reset_index().head(10).to_html(escape=False, index=False), unsafe_allow_html=True)    with tab_configurations:    #with col_configs:        st.subheader("Most Consuming Configurations")        st.write(most_consuming_configs.loc[:, ['config_link','kbc_component_id', 'time_credits_used', 'njobs']].head(10).to_html(escape=False, index=False), unsafe_allow_html=True)except KeyError:    logging.warning("Organization / Project not used")