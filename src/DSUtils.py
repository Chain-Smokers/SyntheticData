import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class DSUtils:
    @staticmethod
    def createDatasetForVoterData(votersDetailed, nodeAddresses):
        dict = {"name": [voter[0] for voter in votersDetailed], "has_cast_vote": [voter[1] for voter in votersDetailed], "is_logged_in": [voter[2] for voter in votersDetailed],
                "password": [voter[3] for voter in votersDetailed], "node_address": [voter[4] for voter in votersDetailed], "timestamp": [voter[5] for voter in votersDetailed]}
        df = pd.DataFrame.from_dict(dict).set_index('name')
        df['node_address'].replace(['0x0000000000000000000000000000000000000000']+nodeAddresses, [
            None]+[f'Norm{i}' for i in range(1, len(nodeAddresses)+1)], inplace=True)

        df['timestamp'].replace(0, np.NaN, inplace=True)
        df['Date/Time'] = pd.to_datetime(df['timestamp'], unit='s')
        df['HourOfDay'] = df['Date/Time'].dt.hour
        return df

    @staticmethod
    def __make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d} ({p:.0f}%)'.format(p=pct, v=val)
        return my_autopct

    @staticmethod
    def nodewiseVotingGraph(df):
        fig, ax = plt.subplots()
        df2 = df.groupby(['node_address'])[
            'node_address'].count().reset_index(name='votes')

        patches, texts, autotexts = ax.pie(
            df2['votes'], labels=df2['node_address'], autopct=DSUtils.__make_autopct(df2['votes']))
        ax.legend(patches, df2['node_address'], loc="center right",
                  title='nodes', bbox_to_anchor=(1.35, 0.5))
        ax.set_title("Node-wise voting")
        return fig

    @staticmethod
    def timewiseVotingGraph(df):
        fig, ax = plt.subplots()
        fig, ax = plt.subplots()
        df2 = df.groupby(['HourOfDay'])[
            'HourOfDay'].count().reset_index(name='votes')
        df2['HourOfDay'] = [int(x) for x in df2['HourOfDay']]

        ax.hist(df2['HourOfDay'], weights=df2['votes'], bins=range(
            min(df2['HourOfDay']), max(df2['HourOfDay'])+2, 1))
        ax.set_xlabel('Time (Hours)')
        ax.set_ylabel('Votes')
        ax.set_title("Time v/s votes")
        return fig

    @staticmethod
    def percentageVotingGraph(df):
        fig, ax = plt.subplots()
        df2 = df.groupby(['has_cast_vote'])[
            'has_cast_vote'].count().reset_index(name='votes')
        patches, texts, autotexts = ax.pie(
            df2['votes'], labels=df2['has_cast_vote'], autopct=DSUtils.__make_autopct(df2['votes']))
        ax.legend(patches, df2['has_cast_vote'], loc="center right",
                  title='has cast vote?', bbox_to_anchor=(1.35, 0.5))
        ax.set_title("Percentage voting")
        return fig
