{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 项目：用逻辑回归预测泰坦尼克号幸存情况"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 分析目标"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "此数据分析报告的目的是，基于泰坦尼克号乘客的性别和船舱等级等属性，对幸存情况进行逻辑回归分析，从而能利用得到的模型，对未知幸存情况的乘客，根据属性预测是否从沉船事件中幸存。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 简介"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> 泰坦尼克号（英语：RMS Titanic）是一艘奥林匹克级邮轮，于1912年4月首航时撞上冰山后沉没。泰坦尼克号是同级的3艘超级邮轮中的第2艘，与姐妹船奥林匹克号和不列颠号为白星航运公司的乘客们提供大西洋旅行。\n",
    "\n",
    "> 泰坦尼克号由位于北爱尔兰贝尔法斯特的哈兰·沃尔夫船厂兴建，是当时最大的客运轮船，由于其规模相当一艘现代航空母舰，因而号称“上帝也沉没不了的巨型邮轮”。在泰坦尼克号的首航中，从英国南安普敦出发，途经法国瑟堡-奥克特维尔以及爱尔兰昆士敦，计划横渡大西洋前往美国纽约市。但因为人为错误，于1912年4月14日船上时间夜里11点40分撞上冰山；2小时40分钟后，即4月15日凌晨02点20分，船裂成两半后沉入大西洋，死亡人数超越1500人，堪称20世纪最大的海难事件，同时也是最广为人知的海难之一。\n",
    "\n",
    "数据集包括两个数据表：`titianic_train.csv`和`titanic_test.csv`。\n",
    "\n",
    "`titianic_train.csv`记录了超过八百位泰坦尼克号乘客在沉船事件后的幸存情况，以及乘客的相关信息，包括所在船舱等级、性别、年龄、同乘伴侣/同胞数量、同乘父母/孩子数量，等等。\n",
    "\n",
    "`titanic_test.csv`只包含乘客（这些乘客不在`titianic_train.csv`里）相关信息，此文件可以被用于预测乘客是否幸存。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "`titianic_train.csv`每列的含义如下：\n",
    "- PassengerId：乘客ID\n",
    "- survival：是否幸存\n",
    "   - 0\t否\n",
    "   - 1\t是\n",
    "- pclass：船舱等级\n",
    "   - 1\t一等舱\n",
    "   - 2\t二等舱\n",
    "   - 3  三等舱\n",
    "- sex：性别\n",
    "- Age：年龄\n",
    "- sibsp：同乘伴侣/同胞数量\n",
    "- parch：同乘父母/孩子数量\n",
    "- ticket：船票号\n",
    "- fare：票价金额\n",
    "- cabin：船舱号\n",
    "- embarked：登船港口\n",
    "   - C  瑟堡\n",
    "   - Q  皇后镇\n",
    "   - S  南安普敦\n",
    "   \n",
    "   \n",
    "`titianic_test.csv`每列的含义和上面相同，但不具备survival变量的数据，即是否幸存。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 读取数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "导入数据分析所需要的库。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "我们计划先利用`titanic_train.csv`训练预测模型，因此读取数据方面，当前只需要导入`titanic_train.csv`。\n",
    "\n",
    "通过Pandas的`read_csv`函数，将原始数据文件`titanic_train.csv`里的数据内容，解析为DataFrame并赋值给变量`original_titanic_train`。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Braund, Mr. Owen Harris</td>\n",
       "      <td>male</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>A/5 21171</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>\n",
       "      <td>female</td>\n",
       "      <td>38.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>PC 17599</td>\n",
       "      <td>71.2833</td>\n",
       "      <td>C85</td>\n",
       "      <td>C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Heikkinen, Miss. Laina</td>\n",
       "      <td>female</td>\n",
       "      <td>26.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>STON/O2. 3101282</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>\n",
       "      <td>female</td>\n",
       "      <td>35.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>113803</td>\n",
       "      <td>53.1000</td>\n",
       "      <td>C123</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Allen, Mr. William Henry</td>\n",
       "      <td>male</td>\n",
       "      <td>35.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>373450</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   PassengerId  Survived  Pclass  \\\n",
       "0            1         0       3   \n",
       "1            2         1       1   \n",
       "2            3         1       3   \n",
       "3            4         1       1   \n",
       "4            5         0       3   \n",
       "\n",
       "                                                Name     Sex   Age  SibSp  \\\n",
       "0                            Braund, Mr. Owen Harris    male  22.0      1   \n",
       "1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  38.0      1   \n",
       "2                             Heikkinen, Miss. Laina  female  26.0      0   \n",
       "3       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  35.0      1   \n",
       "4                           Allen, Mr. William Henry    male  35.0      0   \n",
       "\n",
       "   Parch            Ticket     Fare Cabin Embarked  \n",
       "0      0         A/5 21171   7.2500   NaN        S  \n",
       "1      0          PC 17599  71.2833   C85        C  \n",
       "2      0  STON/O2. 3101282   7.9250   NaN        S  \n",
       "3      0            113803  53.1000  C123        S  \n",
       "4      0            373450   8.0500   NaN        S  "
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "original_titanic_train = pd.read_csv(\"titanic_train.csv\")\n",
    "original_titanic_train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 评估和清理数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "在这一部分中，我们将对在上一部分建立的`original_titanic_train`DataFrame所包含的数据进行评估和清理。\n",
    "\n",
    "主要从两个方面进行：结构和内容，即整齐度和干净度。\n",
    "\n",
    "数据的结构性问题指不符合“每个变量为一列，每个观察值为一行，每种类型的观察单位为一个表格”这三个标准；数据的内容性问题包括存在丢失数据、重复数据、无效数据等。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "为了区分开经过清理的数据和原始的数据，我们创建新的变量`cleaned_titanic_train`，让它为`original_titanic_train`复制出的副本。我们之后的清理步骤都将被运用在`cleaned_titanic_train`上。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "cleaned_titanic_train = original_titanic_train.copy()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 数据整齐度"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Braund, Mr. Owen Harris</td>\n",
       "      <td>male</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>A/5 21171</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>\n",
       "      <td>female</td>\n",
       "      <td>38.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>PC 17599</td>\n",
       "      <td>71.2833</td>\n",
       "      <td>C85</td>\n",
       "      <td>C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Heikkinen, Miss. Laina</td>\n",
       "      <td>female</td>\n",
       "      <td>26.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>STON/O2. 3101282</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>\n",
       "      <td>female</td>\n",
       "      <td>35.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>113803</td>\n",
       "      <td>53.1000</td>\n",
       "      <td>C123</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Allen, Mr. William Henry</td>\n",
       "      <td>male</td>\n",
       "      <td>35.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>373450</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Moran, Mr. James</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330877</td>\n",
       "      <td>8.4583</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>McCarthy, Mr. Timothy J</td>\n",
       "      <td>male</td>\n",
       "      <td>54.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>17463</td>\n",
       "      <td>51.8625</td>\n",
       "      <td>E46</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>8</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Palsson, Master. Gosta Leonard</td>\n",
       "      <td>male</td>\n",
       "      <td>2.0</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>349909</td>\n",
       "      <td>21.0750</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>9</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)</td>\n",
       "      <td>female</td>\n",
       "      <td>27.0</td>\n",
       "      <td>0</td>\n",
       "      <td>2</td>\n",
       "      <td>347742</td>\n",
       "      <td>11.1333</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>10</td>\n",
       "      <td>1</td>\n",
       "      <td>2</td>\n",
       "      <td>Nasser, Mrs. Nicholas (Adele Achem)</td>\n",
       "      <td>female</td>\n",
       "      <td>14.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>237736</td>\n",
       "      <td>30.0708</td>\n",
       "      <td>NaN</td>\n",
       "      <td>C</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   PassengerId  Survived  Pclass  \\\n",
       "0            1         0       3   \n",
       "1            2         1       1   \n",
       "2            3         1       3   \n",
       "3            4         1       1   \n",
       "4            5         0       3   \n",
       "5            6         0       3   \n",
       "6            7         0       1   \n",
       "7            8         0       3   \n",
       "8            9         1       3   \n",
       "9           10         1       2   \n",
       "\n",
       "                                                Name     Sex   Age  SibSp  \\\n",
       "0                            Braund, Mr. Owen Harris    male  22.0      1   \n",
       "1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  38.0      1   \n",
       "2                             Heikkinen, Miss. Laina  female  26.0      0   \n",
       "3       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  35.0      1   \n",
       "4                           Allen, Mr. William Henry    male  35.0      0   \n",
       "5                                   Moran, Mr. James    male   NaN      0   \n",
       "6                            McCarthy, Mr. Timothy J    male  54.0      0   \n",
       "7                     Palsson, Master. Gosta Leonard    male   2.0      3   \n",
       "8  Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)  female  27.0      0   \n",
       "9                Nasser, Mrs. Nicholas (Adele Achem)  female  14.0      1   \n",
       "\n",
       "   Parch            Ticket     Fare Cabin Embarked  \n",
       "0      0         A/5 21171   7.2500   NaN        S  \n",
       "1      0          PC 17599  71.2833   C85        C  \n",
       "2      0  STON/O2. 3101282   7.9250   NaN        S  \n",
       "3      0            113803  53.1000  C123        S  \n",
       "4      0            373450   8.0500   NaN        S  \n",
       "5      0            330877   8.4583   NaN        Q  \n",
       "6      0             17463  51.8625   E46        S  \n",
       "7      1            349909  21.0750   NaN        S  \n",
       "8      2            347742  11.1333   NaN        S  \n",
       "9      0            237736  30.0708   NaN        C  "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train.head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从头部的10行数据来看，数据符合“每个变量为一列，每个观察值为一行，每种类型的观察单位为一个表格”，因此不存在结构性问题。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 数据干净度"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "接下来通过`info`，对数据内容进行大致了解。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 891 entries, 0 to 890\n",
      "Data columns (total 12 columns):\n",
      " #   Column       Non-Null Count  Dtype  \n",
      "---  ------       --------------  -----  \n",
      " 0   PassengerId  891 non-null    int64  \n",
      " 1   Survived     891 non-null    int64  \n",
      " 2   Pclass       891 non-null    int64  \n",
      " 3   Name         891 non-null    object \n",
      " 4   Sex          891 non-null    object \n",
      " 5   Age          714 non-null    float64\n",
      " 6   SibSp        891 non-null    int64  \n",
      " 7   Parch        891 non-null    int64  \n",
      " 8   Ticket       891 non-null    object \n",
      " 9   Fare         891 non-null    float64\n",
      " 10  Cabin        204 non-null    object \n",
      " 11  Embarked     889 non-null    object \n",
      "dtypes: float64(2), int64(5), object(5)\n",
      "memory usage: 83.7+ KB\n"
     ]
    }
   ],
   "source": [
    "cleaned_titanic_train.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从输出结果来看，`cleaned_titanic_train`共有891条观察值，其中`Age`、`Cabin`和`Embarked`存在缺失值，将在后续进行评估和清理。\n",
    "\n",
    "数据类型方面，`PassengerId`表示乘客ID，数据类型不应为数字，应为字符串，所以需要进行数据格式转换。\n",
    "\n",
    "并且，我们已知`Survived`（是否幸存）、`Pclass`（船舱等级）、`Sex`（性别）、`Embarked`（登船港口）都是分类数据，可以把数据类型都转换为Category。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "cleaned_titanic_train['PassengerId'] = cleaned_titanic_train['PassengerId'].astype('str')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "cleaned_titanic_train['Survived'] = cleaned_titanic_train['Survived'].astype('category')\n",
    "cleaned_titanic_train['Pclass'] = cleaned_titanic_train['Pclass'].astype('category')\n",
    "cleaned_titanic_train['Sex'] = cleaned_titanic_train['Sex'].astype('category')\n",
    "cleaned_titanic_train['Embarked'] = cleaned_titanic_train['Embarked'].astype('category')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 891 entries, 0 to 890\n",
      "Data columns (total 12 columns):\n",
      " #   Column       Non-Null Count  Dtype   \n",
      "---  ------       --------------  -----   \n",
      " 0   PassengerId  891 non-null    object  \n",
      " 1   Survived     891 non-null    category\n",
      " 2   Pclass       891 non-null    category\n",
      " 3   Name         891 non-null    object  \n",
      " 4   Sex          891 non-null    category\n",
      " 5   Age          714 non-null    float64 \n",
      " 6   SibSp        891 non-null    int64   \n",
      " 7   Parch        891 non-null    int64   \n",
      " 8   Ticket       891 non-null    object  \n",
      " 9   Fare         891 non-null    float64 \n",
      " 10  Cabin        204 non-null    object  \n",
      " 11  Embarked     889 non-null    category\n",
      "dtypes: category(4), float64(2), int64(2), object(4)\n",
      "memory usage: 59.8+ KB\n"
     ]
    }
   ],
   "source": [
    "cleaned_titanic_train.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 处理缺失数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从`info`方法的输出结果来看，在`cleaned_titanic_train`中，`Age`、`Cabin`和`Embarked`变量存在缺失值。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Moran, Mr. James</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330877</td>\n",
       "      <td>8.4583</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>17</th>\n",
       "      <td>18</td>\n",
       "      <td>1</td>\n",
       "      <td>2</td>\n",
       "      <td>Williams, Mr. Charles Eugene</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>244373</td>\n",
       "      <td>13.0000</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>19</th>\n",
       "      <td>20</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Masselmani, Mrs. Fatima</td>\n",
       "      <td>female</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2649</td>\n",
       "      <td>7.2250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>26</th>\n",
       "      <td>27</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Emir, Mr. Farred Chehab</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2631</td>\n",
       "      <td>7.2250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>28</th>\n",
       "      <td>29</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>O'Dwyer, Miss. Ellen \"Nellie\"</td>\n",
       "      <td>female</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330959</td>\n",
       "      <td>7.8792</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>859</th>\n",
       "      <td>860</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Razi, Mr. Raihed</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2629</td>\n",
       "      <td>7.2292</td>\n",
       "      <td>NaN</td>\n",
       "      <td>C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>863</th>\n",
       "      <td>864</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Sage, Miss. Dorothy Edith \"Dolly\"</td>\n",
       "      <td>female</td>\n",
       "      <td>NaN</td>\n",
       "      <td>8</td>\n",
       "      <td>2</td>\n",
       "      <td>CA. 2343</td>\n",
       "      <td>69.5500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>868</th>\n",
       "      <td>869</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>van Melkebeke, Mr. Philemon</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>345777</td>\n",
       "      <td>9.5000</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>878</th>\n",
       "      <td>879</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Laleff, Mr. Kristo</td>\n",
       "      <td>male</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>349217</td>\n",
       "      <td>7.8958</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>888</th>\n",
       "      <td>889</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Johnston, Miss. Catherine Helen \"Carrie\"</td>\n",
       "      <td>female</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1</td>\n",
       "      <td>2</td>\n",
       "      <td>W./C. 6607</td>\n",
       "      <td>23.4500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>177 rows × 12 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "    PassengerId Survived Pclass                                      Name  \\\n",
       "5             6        0      3                          Moran, Mr. James   \n",
       "17           18        1      2              Williams, Mr. Charles Eugene   \n",
       "19           20        1      3                   Masselmani, Mrs. Fatima   \n",
       "26           27        0      3                   Emir, Mr. Farred Chehab   \n",
       "28           29        1      3             O'Dwyer, Miss. Ellen \"Nellie\"   \n",
       "..          ...      ...    ...                                       ...   \n",
       "859         860        0      3                          Razi, Mr. Raihed   \n",
       "863         864        0      3         Sage, Miss. Dorothy Edith \"Dolly\"   \n",
       "868         869        0      3               van Melkebeke, Mr. Philemon   \n",
       "878         879        0      3                        Laleff, Mr. Kristo   \n",
       "888         889        0      3  Johnston, Miss. Catherine Helen \"Carrie\"   \n",
       "\n",
       "        Sex  Age  SibSp  Parch      Ticket     Fare Cabin Embarked  \n",
       "5      male  NaN      0      0      330877   8.4583   NaN        Q  \n",
       "17     male  NaN      0      0      244373  13.0000   NaN        S  \n",
       "19   female  NaN      0      0        2649   7.2250   NaN        C  \n",
       "26     male  NaN      0      0        2631   7.2250   NaN        C  \n",
       "28   female  NaN      0      0      330959   7.8792   NaN        Q  \n",
       "..      ...  ...    ...    ...         ...      ...   ...      ...  \n",
       "859    male  NaN      0      0        2629   7.2292   NaN        C  \n",
       "863  female  NaN      8      2    CA. 2343  69.5500   NaN        S  \n",
       "868    male  NaN      0      0      345777   9.5000   NaN        S  \n",
       "878    male  NaN      0      0      349217   7.8958   NaN        S  \n",
       "888  female  NaN      1      2  W./C. 6607  23.4500   NaN        S  \n",
       "\n",
       "[177 rows x 12 columns]"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[cleaned_titanic_train['Age'].isna()]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "有177条观察值的年龄变量缺失，占总体数据比例20%左右。由于这些观察值数量较多，且的其它变量仍然能为分析提供价值，我们最好保留这些行。\n",
    "\n",
    "但由于我们后面需要用到的逻辑回归函数`Logit`不允许数据中包含缺失值，所以用乘客年龄平均值对缺失值进行填充。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "average_age = cleaned_titanic_train['Age'].mean()\n",
    "cleaned_titanic_train['Age'] = cleaned_titanic_train['Age'].fillna(average_age)\n",
    "cleaned_titanic_train['Age'].isna().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Braund, Mr. Owen Harris</td>\n",
       "      <td>male</td>\n",
       "      <td>22.000000</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>A/5 21171</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Heikkinen, Miss. Laina</td>\n",
       "      <td>female</td>\n",
       "      <td>26.000000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>STON/O2. 3101282</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Allen, Mr. William Henry</td>\n",
       "      <td>male</td>\n",
       "      <td>35.000000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>373450</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Moran, Mr. James</td>\n",
       "      <td>male</td>\n",
       "      <td>29.699118</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330877</td>\n",
       "      <td>8.4583</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>8</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Palsson, Master. Gosta Leonard</td>\n",
       "      <td>male</td>\n",
       "      <td>2.000000</td>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>349909</td>\n",
       "      <td>21.0750</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>884</th>\n",
       "      <td>885</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Sutehall, Mr. Henry Jr</td>\n",
       "      <td>male</td>\n",
       "      <td>25.000000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>SOTON/OQ 392076</td>\n",
       "      <td>7.0500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>885</th>\n",
       "      <td>886</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Rice, Mrs. William (Margaret Norton)</td>\n",
       "      <td>female</td>\n",
       "      <td>39.000000</td>\n",
       "      <td>0</td>\n",
       "      <td>5</td>\n",
       "      <td>382652</td>\n",
       "      <td>29.1250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>886</th>\n",
       "      <td>887</td>\n",
       "      <td>0</td>\n",
       "      <td>2</td>\n",
       "      <td>Montvila, Rev. Juozas</td>\n",
       "      <td>male</td>\n",
       "      <td>27.000000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>211536</td>\n",
       "      <td>13.0000</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>888</th>\n",
       "      <td>889</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Johnston, Miss. Catherine Helen \"Carrie\"</td>\n",
       "      <td>female</td>\n",
       "      <td>29.699118</td>\n",
       "      <td>1</td>\n",
       "      <td>2</td>\n",
       "      <td>W./C. 6607</td>\n",
       "      <td>23.4500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>890</th>\n",
       "      <td>891</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Dooley, Mr. Patrick</td>\n",
       "      <td>male</td>\n",
       "      <td>32.000000</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>370376</td>\n",
       "      <td>7.7500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>687 rows × 12 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "    PassengerId Survived Pclass                                      Name  \\\n",
       "0             1        0      3                   Braund, Mr. Owen Harris   \n",
       "2             3        1      3                    Heikkinen, Miss. Laina   \n",
       "4             5        0      3                  Allen, Mr. William Henry   \n",
       "5             6        0      3                          Moran, Mr. James   \n",
       "7             8        0      3            Palsson, Master. Gosta Leonard   \n",
       "..          ...      ...    ...                                       ...   \n",
       "884         885        0      3                    Sutehall, Mr. Henry Jr   \n",
       "885         886        0      3      Rice, Mrs. William (Margaret Norton)   \n",
       "886         887        0      2                     Montvila, Rev. Juozas   \n",
       "888         889        0      3  Johnston, Miss. Catherine Helen \"Carrie\"   \n",
       "890         891        0      3                       Dooley, Mr. Patrick   \n",
       "\n",
       "        Sex        Age  SibSp  Parch            Ticket     Fare Cabin Embarked  \n",
       "0      male  22.000000      1      0         A/5 21171   7.2500   NaN        S  \n",
       "2    female  26.000000      0      0  STON/O2. 3101282   7.9250   NaN        S  \n",
       "4      male  35.000000      0      0            373450   8.0500   NaN        S  \n",
       "5      male  29.699118      0      0            330877   8.4583   NaN        Q  \n",
       "7      male   2.000000      3      1            349909  21.0750   NaN        S  \n",
       "..      ...        ...    ...    ...               ...      ...   ...      ...  \n",
       "884    male  25.000000      0      0   SOTON/OQ 392076   7.0500   NaN        S  \n",
       "885  female  39.000000      0      5            382652  29.1250   NaN        Q  \n",
       "886    male  27.000000      0      0            211536  13.0000   NaN        S  \n",
       "888  female  29.699118      1      2        W./C. 6607  23.4500   NaN        S  \n",
       "890    male  32.000000      0      0            370376   7.7500   NaN        Q  \n",
       "\n",
       "[687 rows x 12 columns]"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[cleaned_titanic_train['Cabin'].isna()]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "有687条观察值的船舱号变量缺失，说明船舱号数据在大部分观察值中都是未知的，所以不能删除这些观察值。\n",
    "\n",
    "此外，我们认为船舱号并不是影响生还概率的关键因素，不会被纳入逻辑回归的自变量内，即使缺失也不会影响建立模型，因此可以保留这些观察值。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>61</th>\n",
       "      <td>62</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Icard, Miss. Amelie</td>\n",
       "      <td>female</td>\n",
       "      <td>38.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>113572</td>\n",
       "      <td>80.0</td>\n",
       "      <td>B28</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>829</th>\n",
       "      <td>830</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Stone, Mrs. George Nelson (Martha Evelyn)</td>\n",
       "      <td>female</td>\n",
       "      <td>62.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>113572</td>\n",
       "      <td>80.0</td>\n",
       "      <td>B28</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    PassengerId Survived Pclass                                       Name  \\\n",
       "61           62        1      1                        Icard, Miss. Amelie   \n",
       "829         830        1      1  Stone, Mrs. George Nelson (Martha Evelyn)   \n",
       "\n",
       "        Sex   Age  SibSp  Parch  Ticket  Fare Cabin Embarked  \n",
       "61   female  38.0      0      0  113572  80.0   B28      NaN  \n",
       "829  female  62.0      0      0  113572  80.0   B28      NaN  "
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[cleaned_titanic_train['Embarked'].isna()]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "仅有两条观察值的登船港口变量缺失，但我们认为登船港口并不是影响生还概率的关键因素，不会被纳入逻辑回归的自变量内，即使缺失也不会影响建立模型，因此可以保留这些观察值。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 处理重复数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "根据数据变量的含义以及内容来看，`PassengerId`是乘客的唯一标识符，不应该存在重复，因此查看是否存在重复值。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[\"PassengerId\"].duplicated().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "输出结果为0，说明不存在重复值。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 处理不一致数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "不一致数据可能存在于所有分类变量中，我们要查看是否存在不同值实际指代同一目标的情况。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Survived\n",
       "0    549\n",
       "1    342\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[\"Survived\"].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Pclass\n",
       "3    491\n",
       "1    216\n",
       "2    184\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[\"Pclass\"].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Sex\n",
       "male      577\n",
       "female    314\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[\"Sex\"].value_counts()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Embarked\n",
       "S    644\n",
       "C    168\n",
       "Q     77\n",
       "Name: count, dtype: int64"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train[\"Embarked\"].value_counts()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从以上输出结果来看，均不存在不一致数据。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### 处理无效或错误数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "可以通过DataFrame的`describe`方法，对数值统计信息进行快速了解。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Fare</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>891.000000</td>\n",
       "      <td>891.000000</td>\n",
       "      <td>891.000000</td>\n",
       "      <td>891.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>29.699118</td>\n",
       "      <td>0.523008</td>\n",
       "      <td>0.381594</td>\n",
       "      <td>32.204208</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>13.002015</td>\n",
       "      <td>1.102743</td>\n",
       "      <td>0.806057</td>\n",
       "      <td>49.693429</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>0.420000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>22.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>7.910400</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>29.699118</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>14.454200</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>35.000000</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>31.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>80.000000</td>\n",
       "      <td>8.000000</td>\n",
       "      <td>6.000000</td>\n",
       "      <td>512.329200</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "              Age       SibSp       Parch        Fare\n",
       "count  891.000000  891.000000  891.000000  891.000000\n",
       "mean    29.699118    0.523008    0.381594   32.204208\n",
       "std     13.002015    1.102743    0.806057   49.693429\n",
       "min      0.420000    0.000000    0.000000    0.000000\n",
       "25%     22.000000    0.000000    0.000000    7.910400\n",
       "50%     29.699118    0.000000    0.000000   14.454200\n",
       "75%     35.000000    1.000000    0.000000   31.000000\n",
       "max     80.000000    8.000000    6.000000  512.329200"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train.describe()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "乘客年龄平均为30岁左右，最大值为80岁，最小值为0.42岁。同乘伴侣/同胞数量最大值为8个，最小为0个。同乘父母/孩子数量最大值为6个，最小值为0个。船票价格平均为32元，最大值为512元，最小值为0元，猜测0元表示增票。数据不存在脱离现实的数值。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 整理数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "对数据的整理，与分析方向紧密相关。此次数据分析目标是，根据泰坦尼克号乘客的相关信息，预测沉船事件发生后的生还概率。\n",
    "\n",
    "数据变量包含乘客同乘伴侣/同胞数量，以及同乘父母/孩子数量，这些可以帮助计算出船上家庭成员的数量。我们对同乘家庭成员数量是否会显著影响幸存感兴趣，因此可以创建一个新的变量，记录这一数值。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "      <th>FamilyNum</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Braund, Mr. Owen Harris</td>\n",
       "      <td>male</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>A/5 21171</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>\n",
       "      <td>female</td>\n",
       "      <td>38.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>PC 17599</td>\n",
       "      <td>71.2833</td>\n",
       "      <td>C85</td>\n",
       "      <td>C</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Heikkinen, Miss. Laina</td>\n",
       "      <td>female</td>\n",
       "      <td>26.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>STON/O2. 3101282</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>\n",
       "      <td>female</td>\n",
       "      <td>35.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>113803</td>\n",
       "      <td>53.1000</td>\n",
       "      <td>C123</td>\n",
       "      <td>S</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Allen, Mr. William Henry</td>\n",
       "      <td>male</td>\n",
       "      <td>35.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>373450</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  PassengerId Survived Pclass  \\\n",
       "0           1        0      3   \n",
       "1           2        1      1   \n",
       "2           3        1      3   \n",
       "3           4        1      1   \n",
       "4           5        0      3   \n",
       "\n",
       "                                                Name     Sex   Age  SibSp  \\\n",
       "0                            Braund, Mr. Owen Harris    male  22.0      1   \n",
       "1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  38.0      1   \n",
       "2                             Heikkinen, Miss. Laina  female  26.0      0   \n",
       "3       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  35.0      1   \n",
       "4                           Allen, Mr. William Henry    male  35.0      0   \n",
       "\n",
       "   Parch            Ticket     Fare Cabin Embarked  FamilyNum  \n",
       "0      0         A/5 21171   7.2500   NaN        S          1  \n",
       "1      0          PC 17599  71.2833   C85        C          1  \n",
       "2      0  STON/O2. 3101282   7.9250   NaN        S          0  \n",
       "3      0            113803  53.1000  C123        S          1  \n",
       "4      0            373450   8.0500   NaN        S          0  "
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cleaned_titanic_train['FamilyNum'] = cleaned_titanic_train['SibSp'] + cleaned_titanic_train['Parch']\n",
    "cleaned_titanic_train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 探索数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "在着手逻辑回归分析之前，我们可以先借助数据可视化，探索数值变量的分布，以及与乘客是否幸存存在相关性的变量，为后续的进一步分析提供方向。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 设置图表色盘为\"pastel\"\n",
    "sns.set_palette(\"pastel\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 设置图表尺寸\n",
    "plt.rcParams[\"figure.figsize\"] = [7.00, 3.50]\n",
    "plt.rcParams[\"figure.autolayout\"] = True"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 幸存比例"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 700x350 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "survived_count = cleaned_titanic_train['Survived'].value_counts()\n",
    "survived_label = survived_count.index\n",
    "plt.pie(survived_count, labels=survived_label, autopct='%.1f%%')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从以上饼图来看，泰坦尼克号遇难乘客多于幸存乘客，比例约为3:2。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 乘客年龄"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAArIAAAFTCAYAAADFie86AAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8g+/7EAAAACXBIWXMAAA9hAAAPYQGoP6dpAABCR0lEQVR4nO3df1xVVb7/8Te/8Qc/xAQkQclM1NQxNWS0tGREMstkKr1UNlk2hpbS7QeVWk6GOVN6LdTqktZjxF9z08pRG8OiSDSlr5paqKVBKmgqHKU4/Dj7+8dczvUoKCBwOOe8no/HfnT2Wuvs81k+YPdhnbXXcjMMwxAAAADgYNztHQAAAADQECSyAAAAcEgksgAAAHBIJLIAAABwSCSyAAAAcEgksgAAAHBIJLIAAABwSCSyAAAAcEgksgAAAHBIJLIAAABwSHZNZFNTUzVw4ED5+fkpODhYY8aMUV5enk2bYcOGyc3Nzeb485//bNMmPz9fo0aNUuvWrRUcHKynnnpKlZWVzdkVAAAANDNPe354VlaWkpKSNHDgQFVWVuq5557TiBEjtH//frVp08ba7pFHHtHs2bOt561bt7a+rqqq0qhRoxQaGqqtW7fq+PHjeuCBB+Tl5aVXXnmlTnFYLBYdO3ZMfn5+cnNza7wOAnA5hmHo7NmzCgsLk7u763zpxX0UQGOp133UaEFOnDhhSDKysrKsZUOHDjWeeOKJWt+zYcMGw93d3SgsLLSWLV682PD39zfMZnOdPregoMCQxMHBwdFoR0FBQYPvhY6I+ygHB0djH3W5j9p1RPZCJSUlkqSgoCCb8uXLl+vvf/+7QkNDNXr0aM2YMcM6KpuTk6PevXsrJCTE2j4uLk6TJ0/Wvn371K9fv4s+x2w2y2w2W88Nw5AkFRQUyN/fv9H7BcB1mEwmhYeHy8/Pz96hNKvq/nIfBXCl6nMfbTGJrMVi0bRp0zR48GBdf/311vL/+I//UOfOnRUWFqY9e/bomWeeUV5enj744ANJUmFhoU0SK8l6XlhYWONnpaam6qWXXrqo3N/fnxswgEbhal+vV/eX+yiAxlKX+2iLSWSTkpK0d+9eZWdn25RPmjTJ+rp3797q2LGjhg8frh9++EFdu3Zt0GelpKQoOTnZel6d+QMAAMBxtIgnEaZMmaL169frs88+U6dOnS7ZNjo6WpJ06NAhSVJoaKiKiops2lSfh4aG1ngNHx8f66gBowcAAACOya6JrGEYmjJlitauXastW7YoMjLysu/ZtWuXJKljx46SpJiYGH377bc6ceKEtc3mzZvl7++vnj17NkncAAAAsD+7Ti1ISkpSRkaGPvzwQ/n5+VnntAYEBKhVq1b64YcflJGRodtuu03t27fXnj17NH36dN18883q06ePJGnEiBHq2bOn7r//fs2bN0+FhYV64YUXlJSUJB8fH3t2DwAAAE3IriOyixcvVklJiYYNG6aOHTtaj1WrVkmSvL299emnn2rEiBGKiorSk08+qYSEBH388cfWa3h4eGj9+vXy8PBQTEyM7rvvPj3wwAM2684CAADA+dh1RLZ62avahIeHKysr67LX6dy5szZs2NBYYQEAgEZmsVh05MgRnT17Vn5+furSpYtLbRqCpsFPEAA4saqqKs2YMUORkZFq1aqVunbtqr/85S82AwmGYWjmzJnq2LGjWrVqpdjYWB08eNCOUcPZ7Nu3T6+//rrS09O1evVqpaen6/XXX9e+ffvsHRocXItZfgsA0PheffVVLV68WO+995569eqlnTt36k9/+pMCAgL0+OOPS5LmzZunhQsX6r333lNkZKRmzJihuLg47d+/X76+vnbuARzdvn37tGLFCnXv3l333HOPQkJCVFRUpKysLK1YsULjx49Xr1697B0mHBQjsgDgxLZu3ao777xTo0aNUpcuXfTHP/5RI0aM0Ndffy3p36OxCxYs0AsvvKA777xTffr00fvvv69jx45p3bp19g0eDs9isWjjxo3q3r27EhMTFRERIR8fH0VERCgxMVHdu3fXxo0bZbFY7B0qHBSJLAA4sd///vfKzMzUgQMHJEm7d+9Wdna24uPjJUmHDx9WYWGhYmNjre8JCAhQdHS0cnJyar2u2WyWyWSyOYALHTlyRGfOnNHQoUMvmg/r7u6uoUOH6syZMzpy5Ih9AoTDY2oBHMLtd9ylk6dOX7JNh/ZBWv/R2maKCHAMzz77rEwmk6KiouTh4aGqqirNmTNHiYmJkv5vK++atvqubZtvqfatvoHznT17VtLFP1/Vqsur2wH1RSILh3Dy1GnN/u9Nl2wz8+GRzRQN4DhWr16t5cuXKyMjQ7169dKuXbs0bdo0hYWFacKECQ2+Llt9oy78/Pwk/XvHzYiIiIvqq3firG4H1BdT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kQUAAE2qtqmEdZliCFwKiSwAAGgS1VvPV+vUqZMefPBBmzXja2oH1BVTCwAAQJO4cMOhn3/+WcuWLbtsO6CuGJEFAABN4qeffmrUdsCFSGQBAECTuHCL+WuvvVaPPPKIrr322ku2A+qKqQUAAKBJBAQEqKioyHp+6NAhHTp0qMZ2QEMwIgsAAJqEn59fo7YDLkQiCwBO7ujRo7rvvvvUvn17tWrVSr1799bOnTut9YZhaObMmerYsaNatWql2NhYm7U+gYa6cDWCwMBA3XPPPQoMDLxkO6CuSGQBwImdOXNGgwcPlpeXlzZu3Kj9+/frtddes9kSdN68eVq4cKGWLFmi7du3q02bNoqLi1NZWZkdI4czuHDKQHFxsVavXn3RnFimFqChmCMLAE7s1VdfVXh4uJYuXWoti4yMtL42DEMLFizQCy+8oDvvvFOS9P777yskJETr1q3TuHHjaryu2WyW2Wy2nrPFKGpy9uzZRm0HXIgRWQBwYh999JEGDBigu+++W8HBwerXr5/eeecda/3hw4dVWFio2NhYa1lAQICio6OVk5NT63VTU1MVEBBgPcLDw5u0H3BMF04ZqG3VAqYWoKFIZAHAif34449avHixunXrpk8++USTJ0/W448/rvfee0+SVFhYKEkKCQmxeV9ISIi1riYpKSkqKSmxHgUFBU3XCTisC+fCHjp0SO+8885FKxdc2A6oK6YWAIATs1gsGjBggF555RVJUr9+/bR3714tWbJEEyZMaPB1fXx85OPj01hhwkl17txZeXl5dWoHNAQjsgDgxDp27KiePXvalPXo0UP5+fmSpNDQUEmyWeuz+ry6DmioC+dOt23bVnfddZfatm17yXZAXZHIAoATGzx48EUjYgcOHLCOgEVGRio0NFSZmZnWepPJpO3btysmJqZZY4XzuTBhPXfunNauXatz585dsh1QVySyAODEpk+frm3btumVV17RoUOHlJGRobfffltJSUmSJDc3N02bNk0vv/yyPvroI3377bd64IEHFBYWpjFjxtg3eDi88/+IcnNzs6k7/7wu0w+AmjBHFgCc2MCBA7V27VqlpKRo9uzZioyM1IIFC5SYmGht8/TTT6u0tFSTJk1ScXGxhgwZok2bNsnX19eOkcMZnL8agWEY6tu3r4YMGaLs7Gzt3r27xnZAfZDIAoCTu/3223X77bfX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3bXOZzabdfTo0SsOCgAAALicej3s9dFHH1lff/LJJwoICLCeV1VVKTMzU126dGm04AAAAIDa1CuRHTNmjCTJzc1NEyZMsKnz8vJSly5d9NprrzVacAAAAEBt6pXIWiwWSVJkZKR27Nihq666qkmCAgAAAC6nQevIHj58uLHjAAAAAOqlwRsiZGZmKjMzUydOnLCO1FZ79913rzgwAAAA4FIatGrBSy+9pBEjRigzM1O//PKLzpw5Y3MAABpHeXm58vLyVFlZae9QAKDFadCI7JIlS7Rs2TLdf//9jR0PAEDSr7/+qqlTp+q9996TJB04cEDXXHONpk6dqquvvlrPPvusnSMEAPtr0IhseXm5fv/73zd2LACA/5WSkqLdu3fr888/l6+vr7U8NjZWq1atsmNkANByNCiRffjhh5WRkdHYsQAA/te6dev05ptvasiQIXJzc7OW9+rVSz/88IMdIwOAlqNBUwvKysr09ttv69NPP1WfPn3k5eVlU//66683SnAA4KpOnjyp4ODgi8pLS0ttElsAcGUNSmT37Nmj3/3ud5KkvXv32tRxgwWAKzdgwAD985//1NSpUyX93731v//7vxUTE2PP0ACgxWhQIvvZZ581dhwAgPO88sorio+P1/79+1VZWan/+q//0v79+7V161ZlZWXZOzwAaBEaNEcWANC0hgwZol27dqmyslK9e/fWv/71LwUHBysnJ0f9+/e3d3gA0CI0aET2lltuueQUgi1btjQ4IADAv3Xt2lXvvPNOo15z7ty5SklJ0RNPPKEFCxZI+vdzD08++aRWrlwps9msuLg4LVq0SCEhIY362QDQ2BqUyFbPj61WUVGhXbt2ae/evZowYUJjxAUALs1kMtVY7ubmJh8fH3l7e9f7mjt27NBbb72lPn362JRPnz5d//znP7VmzRoFBARoypQpGjt2rL766qsGxQ4AzaVBiez8+fNrLH/xxRd17ty5KwoIACAFBgZe8puvTp066cEHH9SsWbPk7n75WWLnzp1TYmKi3nnnHb388svW8pKSEqWnpysjI0O33nqrJGnp0qXq0aOHtm3bpkGDBtV4PbPZLLPZbD2vLfEGgKbUqHNk77vvPr377ruNeUkAcEnLli1TWFiYnnvuOa1bt07r1q3Tc889p6uvvlqLFy/WpEmTtHDhQs2dO7dO10tKStKoUaMUGxtr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AByVm2Gct3UNAAAA4CCYIwsAAACHRCILAAAAh0QiCwAAAIdEIgsAAACHRCILAAAAh0QiCwAAAIdEIgsAAACHRCILAAAAh0QiCwAAAIdEIguXl5OTIw8PD40aNcreoQAAgHpgi1q4vIcfflht27ZVenq68vLyFBYWZu+QAABAHTAiC5d27tw5rVq1SpMnT9aoUaO0bNkym/qPPvpI3bp1k6+vr2655Ra99957cnNzU3FxsbVNdna2brrpJrVq1Urh4eF6/PHHVVpa2rwdAQDABZHIwqWtXr1aUVFR6t69u+677z69++67qv6S4vDhw/rjH/+oMWPGaPfu3Xr00Uf1/PPP27z/hx9+0MiRI5WQkKA9e/Zo1apVys7O1pQpU+zRHQAAXApTC+DSBg8erHvuuUdPPPGEKisr1bFjR61Zs0bDhg3Ts88+q3/+85/69ttvre1feOEFzZkzR2fOnFFgYKAefvhheXh46K233rK2yc7O1tChQ1VaWipfX197dAsAAJfAiCxcVl5enr7++muNHz9ekuTp6al7771X6enp1vqBAwfavOfGG2+0Od+9e7eWLVumtm3bWo+4uDhZLBYdPny4eToCAICL8rR3AIC9pKenq7Ky0ubhLsMw5OPjozfffLNO1zh37pweffRRPf744xfVRURENFqsAADgYiSycEmVlZV6//339dprr2nEiBE2dWPGjNGKFSvUvXt3bdiwwaZux44dNuc33HCD9u/fr2uvvbbJYwYAALaYIwuXtG7dOt177706ceKEAgICbOqeeeYZbdmyRatXr1b37t01ffp0TZw4Ubt27dKTTz6pn3/+WcXFxQoICNCePXs0aNAgPfTQQ3r44YfVpk0b7d+/X5s3b67zqC4AAGgY5sjCJaWnpys2NvaiJFaSEhIStHPnTp09e1b/+Mc/9MEHH6hPnz5avHixddUCHx8fSVKfPn2UlZWlAwcO6KabblK/fv00c+ZM1qIFAKAZMCIL1MOcOXO0ZMkSFRQU2DsUAABcHnNkgUtYtGiRBg4cqPbt2+urr77SX//6V9aIBQCghSCRBS7h4MGDevnll3X69GlFREToySefVEpKir3DAgAAYmoBAAAAHBQPewEAAMAhkcgCAADAIZHIAgAAwCGRyAIAAMAhkcgCAADAIZHIAgAAwCGRyAIAAMAhkcgCAADAIf1/szm7hX+ym2cAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 700x350 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "figure, axes = plt.subplots(1, 2)\n",
    "sns.histplot(cleaned_titanic_train, x='Age', ax=axes[0])\n",
    "sns.boxplot(cleaned_titanic_train, y='Age', ax=axes[1])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "大多数乘客年龄位于20岁到40岁之间，但有不少老年乘客以及婴儿。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 乘客年龄与是否幸存"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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FB4ergceeEAzZsywXfPII4+opKRE999/v6xWq/r06aO1a9eyhizQwAQHmRV5edjvX3geh4LMv38RAMBj1CrIRkREaPfu3fr888+1f/9+SVJ0dLTdMljO0KJFC82ZM0dz5sw55zUmk0kzZ87UzJkznfreAAAAcG8XtWrB+vXr1bFjRxUVFclkMummm27ShAkTNGHCBPXs2VOdOnXSli1b6qpWAAAAwOaiguycOXM0duxYBQQEnHXObDbrgQce0EsvveS04gAAAIBzuaggu2fPHt1yyy3nPH/zzTcrMzPT4aIAAACA33NRQTY/P7/GZbeqeXl56eeff3a4KAAAAOD3XFSQvfzyy7Vv375znt+7d6/dxgQAAABAXbmoIDtw4EClpKSorKzsrHO//vqrnnjiCd16661OKw4AAAA4l4tafmv69OlasWKFrrrqKiUmJqp9+/aSpP3792vu3LmqrKzU448/XieFAgAAAL91UUE2JCREX375pcaNG6fk5GQZhiHpzFquAwYM0Ny5cxUSElInhQIAAAC/ddEbIrRu3VqffPKJjh8/rsOHD8swDLVr106XXnppXdQHAAAA1KhWO3tJ0qWXXqqePXs6sxYAAADggl3UZC8AAADAXRBkAQAA4JEIsgAAAPBIBFkAAAB4JIIsAAAAPBJBFgAAAB6JIAsAAACPRJAFAACARyLIAgAAwCMRZAEAAOCRCLIAAADwSARZAAAAeCS3D7I//vijRowYoZYtW6pZs2a65pprtGvXLtt5wzA0Y8YMhYWFqVmzZoqLi9OhQ4dcWDEAAADqg1sH2ePHj6t3797y9vbWp59+qm+//VYvvviiLr30Uts1zz//vF599VWlpqZq+/btuuSSSzRgwACVlZW5sHIAAADUNS9XF3A+zz33nCIiIrRw4ULbsaioKNufDcPQnDlzNH36dA0ePFiS9M477ygkJESrVq3S8OHD671mAAAA1A+3viO7evVq9ejRQ3/+85/VqlUrde3aVW+99ZbtfE5OjiwWi+Li4mzHzGazYmJilJGR4YqSAQAAUE/cOsh+9913mjdvntq1a6fPPvtM48aN08SJE7Vo0SJJksVikSSFhITYvS4kJMR2ribl5eUqKiqyewAAAMCzuPXQgqqqKvXo0UN///vfJUldu3bVvn37lJqaqpEjR9a63VmzZumpp55yVpkAAABwAbe+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JSUl9ftBAMDJCLIA4Obef/99dejQQe3bt9eIESO0YMECVf8yLScnR3feeaeGDBmiPXv26IEHHtDjjz9u9/ojR47olltu0bBhw7R3716999572rp1qxITE13xcQDAaRhaAABurnfv3rrrrrs0adIknT59WmFhYVq+fLn69u2radOmac2aNfr6669t10+fPl3PPPOMjh8/rsDAQN13331q2rSp/vGPf9iu2bp1q2644QaVlJTIz8/PFR8LABzGHVkAcGMHDhzQjh079Je//EWS5OXlpbvvvlvz58+3ne/Zs6fda3r16mX3fM+ePUpLS1Pz5s1tjwEDBqiqqko5OTn180EAoA54uboAAMC5zZ8/X6dPn7ab3GUYhnx9ffX6669fUBvFxcV64IEHNHHixLPORUZGOq1WAKhvBFkAcFOnT5/WO++8oxdffFE333yz3bkhQ4bo3XffVfv27fXJJ5/Yndu5c6fd827duunbb7/VlVdeWec1A0B9YowsALipVatW6e6771ZBQYHMZrPduUcffVTr16/X+++/r/bt22vKlCkaM2aMsrKyNHXqVP373/+W1WqV2WzW3r17dd1112n06NG67777dMkll+jbb7/VunXrLviuLgC4I8bIAoCbmj9/vuLi4s4KsZI0bNgw7dq1SydPntS//vUvrVixQp07d9a8efNsqxb4+vpKkjp37qxNmzbp4MGD+uMf/6iuXbtqxowZrEULwONxRxYAGphnnnlGqampOnr0qKtLAYA6xRhZAPBwb7zxhnr27KmWLVvqiy++0OzZs1kjFkCjQJAFAA936NAhPf300zp27JgiIyM1depUJScnu7osAKhzDC0AAACAR2KyFwAAADwSQRYAAAAeiSALAAAAj0SQBQAAgEciyAIAAMAjEWQBAADgkQiyAAAA8EgEWQAAAHgkgiwAAAA80v8DqetDTE0Gs6QAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 700x350 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "sns.histplot(cleaned_titanic_train, x='Age', hue='Survived', alpha=0.4)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从乘客年龄直方图来看，只有婴儿群体幸存比例较高，绝大部分其余年龄段都是遇难人数多于幸存人数。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 船票金额分布"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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NXPnzk1lZWVGjhy52/sHAIDOZDsXAAB4n/vqV7+a008/PQceeGBeeeWVfPOb30zPnj3z+c9/PlVVVZk0aVKmTp2a6urqVFZW5pJLLkl9fX1OPPHEJMmpp56akSNH5rzzzsu1116bhoaGXHHFFZk8eXIqKipKfHYAALBzhOgAAPA+96c//Smf//zn88Ybb2TffffNhz/84Tz++OPZd999kyTXX399ysrKctZZZ6WlpSXjx4/PrFmzCs/v2bNn7rnnnlx00UWpr69Pv379csEFF2T69OmlOiUAAOg0QnQAAHifu+OOO952vk+fPpk5c2ZmzpxZtObAAw/Mvffe29mtAQBAydkTHQAAAAAAiihpiH7jjTfmmGOOSWVlZSorK1NfX5/77ruvML9x48ZMnjw5gwYNSv/+/XPWWWelsbGxw2usXLkyp512Wvr27ZvBgwfn8ssvz+bNm3f3qQAAAAAA0A2VNETff//9853vfCeLFi3KU089lZNPPjmf/vSns3Tp0iTJZZddll/+8pe588478/DDD+eVV17JmWeeWXj+li1bctppp6W1tTWPPfZYfvKTn+TWW2/NlVdeWapTAgAAAACgGynpnuinn356h+N/+Id/yI033pjHH388+++/f26++ebMnj07J598cpLklltuyYgRI/L444/nxBNPzP3335/nnnsuDzzwQGpqajJ69OhcffXV+frXv56rrroq5eXlpTgtAAAAAAC6iT1mT/QtW7bkjjvuyIYNG1JfX59FixZl06ZNGTduXKFm+PDhGTZsWBYsWJAkWbBgQY4++ujU1NQUasaPH5/m5ubCanYAAAAAANhRJV2JniRLlixJfX19Nm7cmP79++fnP/95Ro4cmcWLF6e8vDwDBw7sUF9TU5OGhoYkSUNDQ4cAfev81rliWlpa0tLSUjhubm7upLMBAAAAAKA7KflK9COOOCKLFy/OwoULc9FFF+WCCy7Ic889t0vfc8aMGamqqio8DjjggF36fgAAAAAAdE0lD9HLy8tz6KGHZsyYMZkxY0ZGjRqVH/zgB6mtrU1ra2vWrFnTob6xsTG1tbVJktra2jQ2Nm4zv3WumGnTpmXt2rWFx8svv9y5JwUAAAAAQLdQ8hD9r7W1taWlpSVjxoxJ7969M2/evMLc8uXLs3LlytTX1ydJ6uvrs2TJkqxevbpQM3fu3FRWVmbk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TG1tbaHmiSee6PB6jY2NhbntqaioSEVFRSefBQAAAAAA3U1JV6K3t7dnypQp+fnPf54HH3wwBx98cIf5MWPGpHfv3pk3b15hbPny5Vm5cmXq6+uTJPX19VmyZElWr15dqJk7d24qKyszcuTI3XMiAAAAAAB0SyVdiT558uTMnj07d999dwYMGFDYw7yqqip77bVXqqqqMmnSpEydOjXV1dWprKzMJZdckvr6+px44olJklNPPTUjR47Meeedl2uvvTYNDQ254oorMnnyZKvNAQAAAADYKSUN0W+88cYkycc+9rEO47fccku+8IUvJEmuv/76lJWV5ayzzkpLS0vGjx+fWbNmFWp79uyZe+65JxdddFHq6+vTr1+/XHDBBZk+ffruOg0AAAAAALqpkobo7e3t71jTp0+fzJw5MzNnzixac+CBB+bee+/tzNYAAAAAAKC0e6IDAAAAAMCeTIgOAAAAAABFCNEBAAAAAKAIIToAAAAAABQhRAcAAAAAgCKE6AAAAAAAUIQQHQAAAAAAihCiAwAAAABAEUJ0AAB4n7vxxhtzzDHHpLKyMpWVlamvr899991XmN+4cWMmT56cQYMGpX///jnrrLPS2NjY4TVWrlyZ0047LX379s3gwYNz+eWXZ/Pmzbv7VAAAoNMJ0QEA4H1u//33z3e+850sWrQoTz31VE4++eR8+tOfztKlS5Mkl112WX75y1/mzjvvzMMPP5xXXnklZ555ZuH5W7ZsyWmnnZbW1tY89thj+clPfpJbb701V155ZalOCQAAOk2vUjcAAACU1umnn97h+B/+4R9y44035vHHH8/++++fm2++ObNnz87JJ5+cJLnlllsyYsSIPP744znxxBNz//3357nnnssDDzyQmpqajB49OldffXW+/vWv56qrrkp5eXkpTgsAADqFlegAAEDBli1bcscdd2TDhg2pr6/PokWLsmnTpowbN65QM3z48AwbNiwLFixIkixYsCBHH310ampqCjXjx49Pc3NzYTU7AAB0VVaiAwAAWbJkSerr67Nx48b0798/P//5zzNy5MgsXrw45eXlGThwYIf6mpqaNDQ0JEkaGho6BOhb57fOFdPS0pKWlpbCcXNzcyedDQAAdB4r0QEAgBxxxBFZvHhxFi5cmIsuuigXXHBBnnvuuV36njNmzEhVVVXhccABB+zS9wMAgB0hRAcAAFJeXp5DDz00Y8aMyYwZMzJq1Kj84Ac/SG1tbVpbW7NmzZoO9Y2NjamtrU2S1NbWprGxcZv5rXPFTJs2LWvXri08Xn755c49KQAA6ARCdAAAYBttbW1paWnJmDFj0rt378ybN68wt3z58qxcuTL19fVJkvr6+ixZsiSrV68u1MydOzeVlZUZOXJk0feoqKhIZWVlhwcAAOxp7IkOAADvc9OmTcvEiRMzbNiwrFu3LrNnz85DDz2UX//616mqqsqkSZMyderUVFdXp7KyMpdccknq6+tz4oknJklOPfXUjBw5Muedd16uvfbaNDQ05IorrsjkyZNTUVFR4rMDAICdI0QHAID3udWrV+f888/Pq6++mqqqqhxzzDH59a9/nU984hNJkuuvvz5lZWU566yz0tLSkvHjx2fWrFmF5/fs2TP33HNPLrrootTX16dfv3654IILMn369FKdEgAAdBohOgAAvM/dfPPNbzvfp0+fzJw5MzNnzixac+CBB+bee+/t7NYAAKDk7IkOAAAAAABFCNEBAAAAAKAIIToAAAAAABQhRAcAAAAAgCKE6AAAAAAAUIQQHQAAAAAAihCiAwAAAABAEUJ0AAAAAAAoQogOAAAAAABFCNEBAAAAAKAIIToAAAAAABQhRAcAAAAAgCKE6AAAAAAAUIQQHQAAAAAAihCiAwAAAABAEUJ0AAAAAAAoQogOAAAAAABFCNEBAAAAAKAIIToAAAAAABQhRAcAAAAAgCKE6AAAAAAAUIQQHQAAAAAAihCiAwAAAABAEUJ0AAAAAAAoYodC9EMOOSRvvPHGNuNr1qzJIYccstNNAQAAAADAnmCHQvSXXnopW7Zs2Wa8paUlq1at2ummAAAAAABgT9DrvRT/27/9W+HrX//616mqqiocb9myJfPmzctBBx3Uac0BAAAAAEApvacQ/YwzzkiS9OjRIxdccEGHud69e+eggw7K//gf/6PTmgMAAAAAgFJ6TyF6W1tbkuTggw/Ok08+mX322WeXNAUAAAAAAHuC9xSib/Xiiy92dh8AAAAAALDH2aEQPUnmzZuXefPmZfXq1YUV6lv98z//8043BgAAAMDbW79+fW6++easW7cuAwYMyKRJk9K/f/9StwXQrexQiP6tb30r06dPz/HHH5/99tsvPXr06Oy+AACAd+kPf/hDbrnllvzhD3/ID37wgwwePDj33Xdfhg0bliOPPLLU7QGwi8yYMSPr168vHL/11luZMWNG+vfvn2nTppWwM4DuZYdC9Jtuuim33nprzjvvvM7uBwAAeA8efvjhTJw4MWPHjs0jjzySf/iHf8jgwYPzzDPP5Oabb85dd91V6hYB2AX+MkDff//984lPfCJz587Nn/70p6xfvz4zZswQpAN0kh0K0VtbW/OhD32os3sBAADeo7/7u7/LNddck6lTp2bAgAGF8ZNPPjn/+I//WMLOANhV1q9fXwjQr7jiiuy1115JkkMPPTRvvfVWrrnmmkKNrV0Adl7Zjjzpv/7X/5rZs2d3di8AAMB7tGTJkvzN3/zNNuODBw/O66+/XoKOANjVbr755iR/XoG+NUDfaq+99srQoUM71AGwc3ZoJfrGjRvzT//0T3nggQdyzDHHpHfv3h3mr7vuuk5pDgAAeHsDBw7Mq6++moMPPrjD+L//+78XQhQAupd169YlST7xiU9sd/6UU07JT3/600IdADtnh0L03/3udxk9enSS5Nlnn+0w5yajAACw+5x99tn5+te/njvvvDM9evRIW1tb5s+fn69+9as5//zzS90eALvAgAED8tZbb2Xu3Lk59NBDt5mfN29eoQ6AnbdDIfpvfvObzu4DAADYAd/+9rczefLkHHDAAdmyZUtGjhyZLVu25D//5/+cK664otTtAbALTJo0KTNmzMif/vSnvPXWWx22dHnrrbeyatWqQh0AO2+HQnQAAKD02tvb09DQkB/+8Ie58sors2TJkqxfvz7HHntsDjvssFK3B8Au0r9///Tv3z/r16/PNddck6FDh+aUU07JvHnzCgH61hoAdt4Ohegf//jH33bblgcffHCHGwIAAN6d9vb2HHrooVm6dGkOO+ywHHDAAaVuCYDdZNq0aZkxY0bWr1+fVatW5ac//Wlhrn///pk2bVoJuwPoXnYoRN+6H/pWmzZtyuLFi/Pss8/mggsu6Iy+AACAd1BWVpbDDjssb7zxhpXnAO9D06ZNy/r163PzzTdn3bp1GTBgQCZNmmQFOkAn26EQ/frrr9/u+FVXXZX169fvVEMAAMC7953vfCeXX355brzxxhx11FGlbgeA3ax///75yle+Uuo2ALq1Tt0T/dxzz80HP/jBfP/73+/MlwUAAIo4//zz8+abb2bUqFEpLy/vcHO5JGlqaipRZwAA0D10aoi+YMGC9OnTpzNfEgAAeBs33HBDqVsAAIBubYdC9DPPPLPDcXt7e1599dU89dRT+cY3vtEpjQEAAO/MPYkAAGDX2qEQvaqqqsNxWVlZjjjiiEyfPj2nnnpqpzQGAAC8Nxs3bkxra2uHscrKyhJ1AwAA3cMOhei33HJLZ/cBAADsgA0bNuTrX/96fvazn+WNN97YZn7Lli0l6AoAALqPndoTfdGiRVm2bFmS5Mgjj8yxxx7bKU0BAADvzte+9rX85je/yY033pjzzjsvM2fOzKpVq/LjH/843/nOd0rdHgC72ObNm7Nw4cI0NTWluro6dXV16dWrU2+BB/C+t0PfVVevXp2zzz47Dz30UAYOHJgkWbNmTT7+8Y/njjvuyL777tuZPQIAAEX88pe/zE9/+tN87GMfy4UXXpiTTjophx56aA488MDcfvvtOeecc0rdIgC7yJw5czJ//vy0tbV1GBs7dmwmTJhQws4AupeyHXnSJZdcknXr1mXp0qVpampKU1NTnn322TQ3N+e//bf/1tk9AgAARTQ1NeWQQw5J8uf9z5uampIkH/7wh/PII4+UsjUAdqE5c+bk0UcfTd++fXPGGWfk7/7u73LGGWekb9++efTRRzNnzpxStwjQbexQiD5nzpzMmjUrI0aMKIyNHDkyM2fOzH333ddpzQEAAG/vkEMOyYsvvpgkGT58eH72s58l+fMK9a2/NQpA97J58+bMnz8//fv3z+WXX54TTjghAwYMyAknnJDLL788/fv3z/z587N58+ZStwrQLexQiN7W1pbevXtvM967d+8Ov0IEAADsGn/84x/T1taWCy+8MM8880yS5O/+7u8yc+bM9OnTJ5dddlkuv/zyEncJwK6wcOHCtLW1Zdy4cdvsf96rV6+ccsopaWtry8KFC0vUIUD3skMh+sknn5yvfOUreeWVVwpjq1atymWXXZZTTjml05oDAAC277DDDsvrr7+eyy67LP/tv/23fO5zn8vRRx+d559/PrNnz86///u/5ytf+Uqp2wRgF9i6ddfw4cO3O791fGsdADtnh0L0f/zHf0xzc3MOOuigfOADH8gHPvCBHHzwwWlubs6PfvSjzu4RAAD4K+3t7R2O77333mzYsCEHHnhgzjzzzBxzzDEl6gyAXa26ujpJ8vzzz293fuv41joAdk6vdy7Z1gEHHJCnn346DzzwQOEb84gRIzJu3LhObQ4AAACAjurq6jJnzpw88MADOfbYYzts6bJ58+bMmzcvZWVlqaurK2GXAN3He1qJ/uCDD2bkyJFpbm5Ojx498olPfCKXXHJJLrnkkpxwwgk58sgj8+ijj+6qXgEAgP+/Hj16pEePHtuMAdD99erVK2PHjs369evzve99L0888USam5vzxBNP5Hvf+17Wr1+fsWPHbrNfOgA75j19N73hhhvyxS9+MZWVldvMVVVV5f/9f//fXHfddTnppJM6rUEAAGBb7e3t+cIXvpCKiookycaNG/PlL385/fr161D3r//6r6VoD4BdbMKECUmS+fPn5+67787dd9+dJCkrK8tJJ51UmAdg572nEP2ZZ57Jd7/73aLzp556ar7//e/vdFMAAMDbu+CCCzocn3vuuSXqBIBSmTBhQsaNG5eFCxemqakp1dXVqaurswIdoJO9p++qjY2N6d27d/EX69Urr7322k43BQAAvL1bbrml1C0AsAfYurULALvOe9oTfejQoXn22WeLzv/ud7/Lfvvtt9NNAQAAAADAnuA9heif/OQn841vfCMbN27cZu6tt97KN7/5zfyn//SfOq05AAAAAAAopfe0ncsVV1yRf/3Xf83hhx+eKVOm5IgjjkiSPP/885k5c2a2bNmSv//7v98ljQIAAAAAwO72nkL0mpqaPPbYY7nooosybdq0tLe3J0l69OiR8ePHZ+bMmampqdkljQIAAAAAwO72nm/XfOCBB+bee+/Nf/zHf2TFihVpb2/PYYcdlr333ntX9AcAAAAAACXznkP0rfbee++ccMIJndkLAAAAAADsUd7TjUU72yOPPJLTTz89Q4YMSY8ePfKLX/yiw/wXvvCF9OjRo8NjwoQJHWqamppyzjnnpLKyMgMHDsykSZOyfv363XgWAAAAAAB0VyUN0Tds2JBRo0Zl5syZRWsmTJiQV199tfD43//7f3eYP+ecc7J06dLMnTs399xzTx555JF86Utf2tWtAwAAAADwPrDD27l0hokTJ2bixIlvW1NRUZHa2trtzi1btixz5szJk08+meOPPz5J8qMf/Sif/OQn8/3vfz9Dhgzp9J4BAAAAAHj/KOlK9HfjoYceyuDBg3PEEUfkoosuyhtvvFGYW7BgQQYOHFgI0JNk3LhxKSsry8KFC0vRLgAAAAAA3UhJ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0ZNkypQpRbdv2VNVVFTkm9/85jZby9D1ubbdm+vbfbm23Zdr2325tgDg30OAXa1He3t7e6mbAAAAAACAPVFZqRsAAAAAAIA9lRAdAAAAAACKEKIDAAAAAEARQvQSmjlzZg466KD06dMndXV1eeKJJ0rdEu/gkUceyemnn54hQ4akR48e+cUvftFhvr29PVdeeWX222+/7LXXXhk3blxeeOGFDjVNTU0555xzUllZmYEDB2bSpElZv379bjwL/tqMGTNywgknZMCAARk8eHDOOOOMLF++vEPNxo0bM3ny5AwaNCj9+/fPWWedlcbGxg41K1euzGmnnZa+fftm8ODBufzyy7N58+bdeSpsx4033phjjjkmlZWVqaysTH19fe67777CvGvbfXznO99Jjx49cumllxbGXN+u6aqrrkqPHj06PIYPH16Yd10BAIDdSYheIv/yL/+SqVOn5pvf/GaefvrpjBo1KuPHj8/q1atL3RpvY8OGDRk1alRmzpy53flrr702P/zhD3PTTTdl4cKF6devX8aPH5+NGzcWas4555wsXbo0c+fOzT333JNHHnkkX/rSl3bXKbAdDz/8cCZPnpzHH388c+fOzaZNm3Lqqadmw4YNhZrLLrssv/zlL3PnnXfm4YcfziuvvJIzzzyzML9ly5acdtppaW1tzWOPPZaf/OQnufXWW3PllVeW4pT4C/vvv3++853vZNGiRXnqqady8skn59Of/nSWLl2axLXtLp588sn8+Mc/zjHHHNNh3PXtuo488si8+uqrhcdvf/vbwpzrCgAA7FbtlMQHP/jB9smTJxeOt2zZ0j5kyJD2GTNmlLAr3osk7T//+c8Lx21tbe21tbXt3/ve9wpja9asaa+oqGj/3//7f7e3t7e3P/fcc+1J2p988slCzX333dfeo0eP9lWrVu223nl7q1evbk/S/vDDD7e3t//5Ovbu3bv9zjvvLNQsW7asPUn7ggUL2tvb29vvvffe9rKysvaGhoZCzY033theWVnZ3tLSsntPgHe09957t//P//k/XdtuYt26de2HHXZY+9y5c9s/+tGPtn/lK19pb2/3d7cr++Y3v9k+atSo7c65rgAAwO5mJXoJtLa2ZtGiRRk3blxhrKysLOPGjcuCBQtK2Bk748UXX0xDQ0OH61pVVZW6urrCdV2wYEEGDhyY448/vlAzbty4lJWVZeHChbu9Z7Zv7dq1SZLq6uokyaJFi7Jp06YO13b48OEZNmxYh2t79NFHp6amplAzfvz4NDc3F1Y8U3pbtmzJHXfckQ0bNqS+vt617SYmT56c0047rcN1TPzd7epeeOGFDBkyJIccckjOOeecrFy5MonrCgAA7H69St3A+9Hrr7+eLVu2dPg/dklSU1OT559/vkRdsbMaGhqSZLvXdetcQ0NDBg8e3GG+V69eqa6uLtRQWm1tbbn00kszduzYHHXUUUn+fN3Ky8szcODADrV/fW23d+23zlFaS5YsSX19fTZu3Jj+/fvn5z//eUaOHJnFixe7tl3cHXfckaeffjpPPvnkNnP+7nZddXV1ufXWW3PEEUfk1Vdfzbe+9a2cdNJJefbZZ11XAABgtxOiA/yFyZMn59lnn+2w9y5d3xFHHJHFixdn7dq1ueuuu3LBBRfk4YcfLnVb7KSXX345X/nKVzJ37tz06dOn1O3QiSZOnFj4+phjjkldXV0OPPDA/OxnP8tee+1Vws4AAID3I9u5lMA+++yTnj17prGxscN4Y2NjamtrS9QVO2vrtXu761pbW7vNzWM3b96cpqYm134PMGXKlNxzzz35zW9+k/33378wXltbm9bW1qxZs6ZD/V9f2+1d+61zlFZ5eXkOPfTQjBkzJjNmzMioUaPygx/8wLXt4hYtWpTVq1fnuOOOS69evdKrV688/PDD+eEPf5hevXqlpqbG9e0mBg4cmMMPPzwrVqzw9xYAANjthOglUF5enjFjxmTevHmFsba2tsybNy/19fUl7IydcfDBB6e2trbDdW1ubs7ChQsL17W+vj5r1qzJokWLCjUPPvhg2traUldXt9t75s/a29szZcqU/PznP8+DDz6Ygw8+uMP8mDFj0rt37w7Xdvny5Vm5cmWHa7tkyZIOPySZO3duKisrM3LkyN1zIrxrbW1taWlpcW27uFNOOSVLlizJ4sWLC4/jjz8+55xzTuFr17d7WL9+ff7whz9kv/328/cWAADY7WznUiJTp07NBRdckOOPPz4f/OAHc8MNN2TDhg258MILS90ab2P9+vVZsWJF4fjFF1/M4sWLU11dnWHDhuXSSy/NNddck8MOOywHH3xwvvGNb2TIkCE544wzkiQjRozIhAkT8sUvfjE33XRTNm3alClTpuTss8/OkCFDSnRWTJ48ObNnz87dd9+dAQMGFPbLraqqyl577ZWqqqpMmjQpU6dOTXV1dSorK3PJJZekvr4+J554YpLk1FNPzciRI3Peeefl2muvTUNDQ6644opMnjw5FRUVpTy9971p06Zl4sSJGTZsWNatW5fZs2fnoYceyq9//WvXtosbMGBA4d4FW/Xr1y+DBg0qjLu+XdNXv/rVnH766TnwwAPzyiuv5Jvf/GZ69uyZz3/+8/7eAgAAu187JfOjH/2ofdiwYe3l5eXtH/zgB9sff/zxUrfEO/jNb37TnmSbxwUXXNDe3t7e3tbW1v6Nb3yjvaampr2ioqL9lFNOaV++fHmH13jjjTfaP//5z7f379+/vbKysv3CCy9sX7duXQnOhq22d02TtN9yyy2Fmrfeeqv94osvbt97773b+/bt2/43f/M37a+++mqH13nppZfaJ06c2L7XXnu177PPPu1/+7d/275p06bdfDb8tf/yX/5L+4EHHtheXl7evu+++7afcsop7ffff39h3rXtXj760Y+2f+UrXykcu75d0+c+97n2/fbbr728vLx96NCh7Z/73OfaV6xYUZh3XQEAgN2pR3t7e3uJ8nsAAAAAANij2RMdAAAAAACKEKIDAAAAAEARQnQAAAAAAChCiA4AAAAAAEUI0QEAAAAAoAghOgAAAAAAFCFEBwAAAACAIoToAAAAAABQhBAdAAAAAACKEKIDkCT5whe+kB49emzzWLFiRalbAwAAACiZXqVuAIA9x4QJE3LLLbd0GNt3333f02ts2bIlPXr0SFmZn9MCAAAAXZ+EA4CCioqK1NbWdnj84Ac/yNFHH51+/frlgAMOyMUXX5z169cXnnPrrbdm4MCB+bd/+7eMHDkyFRUVWblyZVpaWvLVr341Q4cOTb9+/VJXV5eHHnqodCcHAAAAsAOE6AC8rbKysvzwhz/M0qVL85Of/CQPPvhgvva1r3WoefPNN/Pd7343//N//s8sXbo0gwcPzpQpU7JgwYLccccd+d3vfpfPfvazmTBhQl544YUSnQkAAADAe9ejvb29vdRNAFB6X/jCF3LbbbelT58+hbGJEyfmzjvv7FB311135ctf/nJef/31JH9eiX7hhRdm8eLFGTVqVJJk5cqVOeSQQ7Jy5coMGTKk8Nxx48blgx/8YL797W/vhjMCAAAA2Hn2RAeg4OMf/3huvPHGwnG/fv3ywAMPZMaMGXn++efT3NyczZs3Z+PGjXnzzTfTt2/fJEl5eXmOOeaYwvOWLFmSLVu25PDDD+/w+i0tLRk0aNDuORkAAACATiBEB6CgX79+OfTQQwvHL730Uv7Tf/pPueiii/IP//APqa6uzm9/+9tMmjQpra2thRB9r732So8ePQrPW79+fXr27JlFixalZ8+eHd6jf//+u+dkAAAAADqBEB2AohYtWpS2trb8j//xP1JW9ufbaPzsZz97x+cde+yx2bJlS1avXp2TTjppV7cJAAAAsMu4sSgARR166KHZtGlTfvSjH+WPf/xj/tf/+l+56aab3vF5hx9+eM4555ycf/75+dd//de8+OKLeeKJJzJjxoz86le/2g2dAwAAAHQOIToARY0aNSrXXXddvvvd7+aoo47K7bffnhkzZryr595yyy05//zz87d/+7c54ogjcsYZZ+TJJ5/MsGHDdnHXAAAAAJ2nR3t7e3upmwAAAAAAgD2RlegAAAAAAFCEEB0AAAAAAIoQogMAAAAAQBFCdACA/187diAAAAAAIMjfeoINCiMAAAAYEh0AAAAAAIZEBwAAAACAIdEBAAAAAGBIdAAAAAAAGBIdAAAAAACGRAcAAAAAgCHRAQAAAABgSHQAAAAAABgBqElUG9jUp7wAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 1500x700 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "figure, axes = plt.subplots(1, 2, figsize=[15, 7])\n",
    "sns.histplot(cleaned_titanic_train, x='Fare', ax=axes[0])\n",
    "sns.boxplot(cleaned_titanic_train, y='Fare', ax=axes[1])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "船票金额呈右偏态分布，说明数据集中的大多数船票价格中等，但有一些票价很高的极端值，使得均值被拉高。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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9//+38jLy4uhQ4dGRMTvfve7WLlyZXTu3Dlzh1eXLl1i586d8f7778eWLVti3bp1MWTIkMwx27Ztu1dfjaFJJzrfY+LEifHss8/GwoUL4+ijj95v7Z4vaeXKlXH88cdHcXFxvPHGG7Vq1q9fHxHxqRN/TZ48OSZNmpT5XFFR0eqCqWHDR0R5HZOvFXbtGi++MDuljgAAAODw0qFDh7jooovioosuittuuy3+4R/+Ie6444545ZVXIiJqzctUVVW1z2P89YveIv6cZVxwwQUxY8aMOOuss2LGjBkxfvz4T+2hffv28aUvfSlmzJgRY8aMiRkzZsQVV1yRmTB927ZtMWDAgL0eCYyIOOqoow74mhtSk4ZSSZLEDTfcELNmzYr58+dH796969xnzyRh3bt3j4iIkpKS+N73vhcbNmyIoqKiiIiYM2dO5OXlRd++ffd5jJycnMjJyWmYizhMlW/cGDOfe22/NWMuPjulbgAAAODw17dv33j66aczYc+6devijDPOiIioNel5XcaOHRs333xzXHnllfGHP/whxowZU2f9RRddFEuXLo158+bFd7/73cy2M888M5588skoKiqq9eK4v9a9e/dYvHhxnHvuuRERsXv37igtLY0zzzyz3j0fjCZ9fG/ChAnx+OOPx4wZM6Jz585RVlYWZWVl8fHHH0dExPvvvx/f+c53orS0ND744IN45pln4uqrr45zzz03+vXrFxERw4YNi759+8ZVV10Vv/vd7+KFF16IW2+9NSZMmNDqgycAAACg4W3cuDEuuOCCePzxx+Ptt9+OVatWxVNPPRU/+MEP4rLLLouOHTvGWWedlZnAfMGCBXHrrbfW+/iXX355bN26NcaPHx/nn39+9OjRY7/15557bhQXF8fYsWOjd+/etR7FGzt2bBQWFsZll10Wr7zySqxatSrmz58f//iP/xh//OMfIyLi61//etx9993x9NNPx/Lly+NrX/tabN68+aC+mwPRpKHUQw89FFu2bInzzjsvunfvnlmefPLJiPjzLWgvvfRSDBs2LE4++eS46aabYvTo0fHLX/4yc4w2bdrEs88+G23atImSkpL48pe/HFdffXXcddddTXVZAAAAQAvWqVOnGDJkSNx3331x7rnnxqmnnhq33XZbXHfddfGjH/0oIiIeeeSR2L17dwwYMCBuvPHGWncv1aVz585x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AAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6oRSAAAAAKROKAUAAABA6po0lFq4cGFceuml0aNHj8jKyoqnn3661vZrrrkmsrKyai0jRoyoVbNp06YYO3Zs5OXlRUFBQVx77bWxbdu2FK8CAAAAgAPVpKHU9u3bo3///jF16tRPrRkxYkSsW7cus/zsZz+rtX3s2LGxdOnSmDNnTjz77LOxcOHCuP766xu7dQAAAAAOQdumPPnIkSNj5MiR+63JycmJ4uLifW5btmxZzJ49O958880YOHBgREQ8+OCDcfHFF8e//Mu/RI8ePRq8ZwAAAAAOXbOfU2r+/PlRVFQUJ510UowfPz42btyY2bZo0aIoKCjIBFIREUOHDo3s7OxYvHhxU7QLAAAAQD006Z1SdRkxYkRcfvnl0bt373j//ffjW9/6VowcOTIWLVoUbdq0ibKysigqKqq1T9u2baNLly5RVlb2qcetrKyMysrKzOeKiopGuwYAAAAA9tasQ6kxY8Zk/nzaaadFv3794vjjj4/58+fHhRdeeNDHnTJlStx5550N0SIAAAAAB6HZP77314477rgoLCyMlStXRkREcXFxbNiwoVbN7t27Y9OmTZ86D1VExOTJk2PLli2Z5cMPP2zUvgEAAACo7bAKpf74xz/Gxo0bo3v37hERUVJSEps3b47S0tJMzbx586KmpiaGDBnyqcfJycmJvLy8WgsAAAAA6WnSx/e2bduWuespImLVqlWxZMmS6NKlS3Tp0iXuvPPOGD16dBQXF8f7778fN998c5xwwgkxfPjwiIjo06dPjBgxIq677rqYNm1aVFVVxcSJE2PMmDHevAcAAADQjDXpnVJvvfVWnHHGGXHGGWdERMSkSZPijDPOiNtvvz3atGkTb7/9dvzt3/5tnHjiiXHttdfGgAED4pVXXomcnJzMMZ544ok4+eST48ILL4yL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",
      "text/plain": [
       "<Figure size 1200x500 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.subplots(1, 1, figsize=[12, 5])\n",
    "sns.histplot(cleaned_titanic_train, x='Fare', hue='Survived', alpha=0.4)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 船舱等级与是否幸存的关系"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAqYAAAFUCAYAAAD2yf4QAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8g+/7EAAAACXBIWXMAAA9hAAAPYQGoP6dpAABHtElEQVR4nO3deXxU9aH38c/MJDPZEwJZycYOYTcgplpk3yzFiq1arqJy8coN9mp6K0/6cqlYL17b61IvhfY+FewtebTagi0qiCjgAi7UqICyGQxIJglLMlknycw8f6RMibJnOWdmvu/Xa14wM2fOfE9CmG9+53fOsfh8Ph8iIiIiIgazGh1ARERERARUTEVERETEJFRMRURERMQUVExFRERExBRUTEVERETEFFRMRURERMQUVExFRERExBRUTEVERETEFMKMDiAiIpfG6/Vy9OhRYmNjsVgsRscRETkrn89HbW0t6enpWK1nHxdVMRURCVBHjx4lMzPT6BgiIhfs8OHDZGRknPV5FVMRkQAVGxsLtP1HHxcXZ3AaEZGzc7lcZGZm+v/fOhsVUxGRAHVq931cXJyKqYgEhPNNO9LBTyIiIiJiCiqmIiIiImIKKqYiIiIiYgqaYyoiEuQ8Hg8tLS1GxzCN8PBwbDab0TFE5AxUTEVEgpTP58PpdFJdXW10FNNJSEggNTVV538VMRkVUxGRIHWqlCYnJxMVFaUSRltZb2hooLKyEoC0tDSDE4nI6VRMRUSCkMfj8ZfSnj17Gh3HVCIjIwGorKwkOTlZu/VFTEQHP4mIBKFTc0qjoqIMTmJOp74umnsrYi4qpiIiQUy7789MXxcRc1IxDQErVqxgxIgR/qvD5Ofn8+qrrxodS0RERKQdzTENARkZGTz66KMMGDAAn8/Hs88+y5w5c/joo48YOnSo0fFEJIRs2bKFiRMncvLkSRISErrsfW699Vaqq6tZt25dl72HBI8X368yOsI5XX95ktERuo1GTEPA7NmzmTVrFgMGDGDgwIE88sgjxMTEsGPHDqOjiYhBqqqqWLRoEVlZWTgcDlJTU5k+fTrvvPNOl77vt771LcrLy4mPj+/S9xGRwKQR0xDj8Xh44YUXqK+vJz8/3+g4ImKQuXPn0tzczLPPPkvfvn2pqKhg8+bNHD9+/JLW5/P58Hg8hIWd+2PFbreTmpp6Se8hIsFPI6Yh4tNPPyUmJgaHw8Gdd97J2rVryc3NNTqWiBigurqat956i//8z/9k4sSJZGdnc/nll1NUVMR3v/tdDh06hMVioaSkpN1rLBYLW7ZsAdp2yVssFl599VXy8vJwOBw888wzWCwWPv/883bv98QTT9CvX792r6uursblchEZGfmNOe9r164lNjaWhoYGAA4fPswPfvADEhISSExMZM6cORw6dMi/vMfjobCwkISEBHr27Mm9996Lz+fr/C+ciHQ5FdMQMWjQIEpKSnjvvfdYtGgR8+fPZ8+ePUbHEhEDxMTEEBMTw7p163C73R1a1//5P/+HRx99lM8++4zrr7+eMWPGsGbNmnbLrFmzhh/+8IffeG1cXBzf+c53KC4u/sby1157LVFRUbS0tDB9+nRiY2N56623eOedd4iJiWHGjBk0NzcD8F//9V+sXr2aZ555hrfffpsTJ06wdu3aDm2XiBhDxTRE2O12+vfvT15eHsuWLWPkyJE89dRTRscSEQOEhYWxevVqnn32WRISErjyyiv56U9/yieffHLR61q6dClTp06lX79+JCYmMm/ePP7f//t//uf37dvHzp07mTdv3hlfP2/ePNatW+cfHXW5XLz88sv+5Z9//nm8Xi//9//+X4YPH86QIUNYtWoVZWVl/tHbJ598kqKiIq677jqGDBnCypUrNYdVJECpmIYor9fb4ZESEQlcc+fO5ejRo/zlL39hxowZbNmyhcsuu4zVq1df1HrGjBnT7v6NN97IoUOH/AdXrlmzhssuu4zBgwef8fWzZs0iPDycv/zlLwD86U9/Ii4ujilTpgDw8ccfc+DAAWJjY/0jvYmJiTQ1NXHw4EFqamooLy9n3Lhx/nWGhYV9I5eIBAYd/BQCioqKmDlzJllZWdTW1lJcXMyWLVvYuHGj0dFExEARERFMnTqVqVOncv/99/PP//zPPPjgg7z11lsA7eZpnu0KSdHR0e3up6amMmnSJIqLi7niiisoLi5m0aJFZ81gt9u5/vrrKS4u5sYbb6S4uJgbbrjBfxBVXV0deXl535geAJCUFDqn0BEJFRoxDQGVlZXccsstDBo0iMmTJ/PBBx+wceNGpk6danQ0ETGR3Nxc6uvr/YWvvLzc/9zpB0Kdz7x583j++efZvn07X3zxBTfeeON5l9+wYQO7d+/mjTfeaLfb/7LLLmP//v0kJyfT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HQZPgq92tZ2w/+ThkJ+LmtPgoSzyzM9FWB0MjswhN7IfqfYO7PMXuUin/z8wYsQIxo0bR3Z2Nn/84x+JjDzLP9jzKCoqorCw0H/f5XKRmZnZ4awiImahYhqIbOGQNbrt1tIIlQfaDpaqOgitoXfS/pzKSrZl/+ODPtwSRrYjnSGRfekb0RubpROOjhLpoISEBAYOHMiBAweYOnUqzc3NVFdXtxs1raioOOOc1FMcDgcOh6Mb0oqIGEPFNNCFR7ZdUar3cPB64PghqNjXdmsKjflnvU5U0rvfZSQ7kujryCDDkaIyKqZTV1fHwYMHufnmm8nLyyM8PJzNmzczd+5cAPbu3UtZWRn5+fkGJxURMY6KaTCx2iCpX9tt2My2U09V7GsrqzXO4LoEqj2q7YCwXn2gVx9uiOphdCKRdv793/+d2bNnk52dzdGjR3nwwQex2WzcdNNNxMfHs2DBAgoLC0lMTCQuLo677rqL/Px8HZEvIiFNxTSYxae13bi67bKndceg5ihUl7f96aoAb6vRKc8vLALikiE2ue18rwnpEJsCFovRyUTO6siRI9x0000cP36cpKQkrrrqKnbs2EFSUhIATzzxBFarlblz5+J2u5k+fTq//vWvDU4tImIsFdNQYbFAbFLbLWNk22NeL9RWtpXUmvK2otrkAnddW5Ht9oxWiE78RwE99WdkfPdnEemg55577pzPR0REsHz5cpYvX95NiUREzE/FtJPV1dVx4MAB//3S0lJKSkpITEwkKyvLwGRnYLVCfGrb7XQ+b1s5baxtK6pNp/489fda8LQC3rZy6/P94+/42l5/qthaLBAe1bbr3R4FjiiwR4M98u9/nno8GqISwaZ/kiIiIqFKLaCTffjhh0ycONF//9SpXebPn8/q1asNSnWRLFaIiGu70fvS1+PzAhbtchcREZELomLaySZMmIDPiN3gZqSrKYmIiMhFUHMQEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVETHQ8uXLycnJISIignHjxvH+++8bHUlExDAqpiIiBnn++ecpLCzkwQcf5G9/+xsjR45k+vTpVFZWGh1NRMQQKqYiIgZ5/PHHWbhwIbfddhu5ubmsXLmSqKgonnnmGaOjiYgYQsVURMQAzc3N7Ny5kylTpvgfs1qtTJkyhe3btxuYTETEOGFGBxARCUXHjh3D4/GQkpLS7vGUlBQ+//zzM77G7Xbjdrv992tqagBwuVznfb+GutoOpO16rvpGoyOck/UCvsYXQ9+PjtH3w1wu5Ptx6v8pn893zuVUTEVEAsSyZct46KGHvvF4ZmamAWlCzRKjA0g7+n6Yy4V/P2pra4mPjz/r8yqmIiIG6NWrFzabjYqKinaPV1RUkJqaesbXFBUVUVhY6L/v9Xo5ceIEPXv2xGKxdGneruRyucjMzOTw4cPExcUZHSfk6fthLsHy/fD5fNTW1pKenn7O5VRMRUQMYLfbycvLY/PmzVx77bVAW9HcvHkzixcvPuNrHA4HDoej3WMJCQldnLT7xMXFBfQHb7DR98NcguH7ca6R0lNUTEVEDFJYWMj8+fMZM2YMl19+OU8++ST19fXcdtttRkcTETGEiqmIiEFuuOEGqqqqeOCBB3A6nYwaNYoNGzZ844AoEZFQoWIqImKgxYsXn3XXfahwOBw8+OCD35imIMbQ98NcQu37YfGd77h9EREREZFuoBPsi4iIiIgpqJiKiIiIiCmomIqIiIiIKaiYioiIIbZt28bs2bNJT0/HYrGwbt06oyOFrGXLljF27FhiY2NJTk7m2muvZe/evUbHClkrVqxgxIgR/nOX5ufn8+qrrxodq1uomIqIiCHq6+sZOXIky5cvNzpKyNu6dSsFBQXs2LGDTZs20dLSwrRp06ivrzc6WkjKyMjg0UcfZefOnXz44YdMmjSJOXPmsHv3bqOjdTkdlS8iIoazWCysXbvWfxUsMVZVVRXJycls3bqV8ePHGx1HgMTERH7xi1+wYMECo6N0KZ3HVERERNqpqakB2sqQGMvj8fDCCy9QX19Pfn6+0XG6nIqpiIiI+Hm9Xu6++26uvPJKhg0bZnSckPXpp5+Sn59PU1MTMTExrF27ltzcXKNjdTkVUxEREfErKChg165dvP3220ZHCWmDBg2ipKSEmpoaXnzxRebPn8/WrVuDvpyqmIqIiAjQdonc9evXs23bNjIyMoyOE9Lsdjv9+/cHIC8vjw8++ICnnnqK3/zmNwYn61oqpiIiIiHO5/Nx1113sXbtWrZs2UKfPn2MjiRf4/V6cbvdRsfociqmIiJiiLq6Og4cOOC/X1paSklJCYmJiWRlZRmYLPQUFBRQXFzMSy+9RGxsLE6nE4D4+HgiIyMNThd6ioqKmDlzJllZWdTW1lJcXMyWLVvYuHGj0dG6nE4XJSIihtiyZQsTJ078xuPz589n9erV3R8ohFksljM+vmrVKm699dbuDSMsWLCAzZs3U15eTnx8PCNGjGDJkiVMnTrV6GhdTsVURERERExBV34SEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERERFTUDEVEREREVNQMRURERERU1AxFRERCWETJkzg7rvvNjqGCKBiKiIiEvBuvfVWLBYLFosFu91O//79Wbp0Ka2trUZHE7koYUYHEBERkY6bMWMGq1atwu1288orr1BQUEB4eDhFRUVGRxO5YBoxFRERCQIOh4PU1FSys7NZtGgRU6ZM4S9/+QsA77zzDhMmTCAqKooePXowffp0Tp48ecb1/O///i9jxowhNjaW1NRUfvjDH1JZWel//uTJk8ybN4+kpCQiIyMZMGAAq1atAqC5uZnFixeTlpZGREQE2dnZLFu2rOs3XoKGRkxFRESCUGRkJMePH6ekpITJkydz++2389RTTxEWFsabb76Jx+M54+taWlp4+OGHGTRoEJWVlRQWFnLrrbfyyiuvAHD//fezZ88eXn31VXr16sWBAwdobGwE4Fe/+hV/+ctf+OMf/0hWVhaHDx/m8OHD3bbNEvhUTEVERIKIz+dj8+bNbNy4kbvuuovHHnuMMWPG8Otf/9q/zNChQ8/6+ttvv93/9759+/KrX/2KsWPHUldXR0xMDGVlZYwePZoxY8YAkJOT41++rKyMAQMGcNVVV2GxWMjOzu78DZSgpl35IiIiQWD9+vXExMQQERHBzJkzueGGG/jZz37mHzG9UDt37mT27NlkZWURGxvL1VdfDbSVToBFixbx3HPPMWrUKO69917effdd/2tvvfVWSkpKGDRoED/60Y947bXXOncjJeipmIqIiASBiRMnUlJSwv79+2lsbOTZZ58lOjqayMjIC15HfX0906dPJy4ujjVr1vDBBx+wdu1aoG3+KMDMmTP58ssvueeeezh69CiTJ0/m3//93wG47LLLKC0t5eGHH6axsZEf/OAHXH/99Z2/sRK0VExFRESCQHR0NP379ycrK4uwsH/M1BsxYgSbN2++oHV8/vnnHD9+nEcffZRvf/vbDB48uN2BT6ckJSUxf/58/vCHP/Dkk0/y29/+1v9cXFwcN9xwA//zP//D888/z5/+9CdOnDjR8Q2UkKA5piIiIkGsqKiI4cOH86//+q/ceeed2O123nzzTb7//e/Tq1evdstmZWVht9t5+umnufPOO9m1axcPP/xwu2UeeOAB8vLyGDp0KG63m/Xr1zNkyBAAHn/8cdLS0hg9ejRWq5UXXniB1NRUEhISumtzJcBpxFRERCSIDRw4kNdee42PP/6Yyy+/nPz8fF566aV2o6qnJCUlsXr1al544QVyc3N59NFH+eUvf9luGbvdTlFRESNGjGD8+PHYbDaee+45AGJjY/0HW40dO5ZDhw7xyiuvYLWqbsiFsfh8Pp/RIURERERE9CuMiIiIiJiCiqmIiIiImIKKqYiIiIiYgoqpiIiIiJiCiqmIiIiImIKKqYiIiIiYgoqpiIiIiJiCiqmIiIiImIKKqYiIiIiYgoqpiIiIiJiCiqmIiIiImIKKqYiIiIiYwv8Hnd19fiBSsV4AAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 700x350 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "figure, axes = plt.subplots(1, 2)\n",
    "pclass_count = cleaned_titanic_train['Pclass'].value_counts()\n",
    "pclass_label = pclass_count.index\n",
    "axes[0].pie(pclass_count, labels=pclass_label)\n",
    "sns.countplot(cleaned_titanic_train, x='Pclass', hue='Survived', ax=axes[1])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从是否幸存与船舱等级之间的柱状图来看，船舱等级低的乘客中遇难比例更大，船舱等级高的乘客中幸存比例更大。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 性别与是否幸存的关系"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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ExERaWihnRwksCyW/4TR8PmxevTRR0lOTiYnJ4fvvvuOhIQEevbsyf3333/Gz2m1WlmwYAF33nknnTt3pn379syYMYP+/fuf8DEZGRmsWrWKKVOmMHjwYFwuFy1btmTo0KF1zuIXERExI4vP5/Od+jARETGb0tJS4uPjKSkpwek8/ZUp3lq3vxGqMq+BhxYYXUJAJQydaMjr6ucqtJ3pz1V9/16pKUVERERETEHBVERERERMQcFURERERExBwVRERERETEHBVERERERMQcFURERERExBwVRERERETEHBVERERERMQcFURERERExBwVRERERETEHBVERERERMQcFURERERExBwVRERERETEHBVERERERMQcFURERERExBwVRERERETEHBVERERERMQcFURERERExBwVRERERETEHBVERERERMQcFURMRAM2fOpFWrVkRFRdGnTx/WrVtndEkiIoZRMBURMcibb77J5MmTeeihh/jiiy/o1q0bQ4YMoaioyOjSREQMoWAqImKQv/zlL9x+++3ceuutdOrUiVmzZhETE8OcOXOMLk1ExBAKpiIiBnC73WzYsIGBAwf6t1mtVgYOHMiaNWsMrExExDgRRhcgIhKODhw4gMfjITU1tdb21NRUtm3bVudjXC4XLpfLf7+kpASA0tLSM6qhouzIGT0uWJWWHzW6hICynuHPxdnSz1VoO9Ofq2N/p3w+30mPUzAVEQkSOTk5/PnPfz5ue2ZmpgHViPlNMboACUln93N15MgR4uPjT7hfwVRExADNmjXDZrNRWFhYa3thYSFpaWl1Pmbq1KlMnjzZf9/r9XLo0CGSkpKwWCyNWm+wKy0tJTMzkz179uB0Oo0uR0KEfq7qz+fzceTIETIyMk56nIKpiIgB7HY7vXr1YunSpQwfPhyoCZpLly5lwoQJdT7G4XDgcDhqbUtISGjkSkOL0+lUgJAGp5+r+jlZS+kxCqYiIgaZPHkyo0ePpnfv3lxwwQVMnz6d8vJybr31VqNLExExhIKpiIhBbrzxRvbv38+0adMoKCige/fuLFmy5LgJUSIi4ULBVETEQBMmTDhh1700HIfDwUMPPXTcUAiRs6Gfq4Zn8Z1q3r6IiIiISABogX0RERERMQUFUxERERExBQVTERERETEFBVMREQlpM2fOpFWrVkRFRdGnTx/WrVtndEkS5D79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",
      "text/plain": [
       "<Figure size 700x350 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "figure, axes = plt.subplots(1, 2)\n",
    "sex_count = cleaned_titanic_train['Sex'].value_counts()\n",
    "sex_label = sex_count.index\n",
    "axes[0].pie(sex_count, labels=sex_label)\n",
    "sns.countplot(cleaned_titanic_train, x='Survived', hue='Sex', ax=axes[1])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从是否幸存与性别之间的柱状图来看，男性乘客中遇难比例更大，女性乘客中幸存比例更大。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 登船港口与是否幸存的关系"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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kaiaq3M6nVKXQAGILaZEREQyotFoYDQafW49evQAAAiCgNdffx0zZsxAWFgY0tLSUFRUhNOnT2Ps2LEIDw/H7bffjtLS0iv2+/rrryMpKQlhYWG47777UF9f71339ddfY9KkSYiJiUFkZCTuuusufPPNNz6PFwQBq1evxo9//GOEh4djxYoVVxyjubkZU6dOxR133OHt3v/zn/+MtLQ0aLVapKam4rXXXvN5zL59+zBs2DBotVqMGDECBw8evNmXkPwYgykREZEfef755zF37lwUFxcjNTUVDz74IP7jP/4D+fn52L9/P0RRxKJFi3wec/r0afzf//0fPvroI2zZsgUHDx7Eo48+6l3f0NCAnJwcfPnll9i7dy/69euHadOmoaGhwWc/zz77LH7yk5/gyJEjePjhh33WWSwWTJo0CR6PB9u3b4fBYMCGDRuwdOlSrFixAiUlJfjNb36DZ555BuvXrwcANDY2YsaMGUhPT8eBAwfw7LPP4r/+67+66JUjvyASERGRLOTk5IhKpVIMDw/3ua1YsUIURVEEIC5ZssS7fVFRkQhAfOONN7zL3nrrLVGr1XrvL1u2TFQqleK5c+e8yz755BNRoVCIlZWVbdbhdrvFiIgI8aOPPvIuAyA+8cQTPtt9/vnnIgCxpKREzMjIELOzs0W73e5d36dPH3Hjxo0+j3n++edFk8kkiqIovv7662J0dLTY0tLiXb969WoRgHjw4MHrvl4UeHiOKRERkYyMGzcOq1ev9lkWFRXl/T4jI8P7fXx8PABg8ODBPstsNhusViv0ej0AIDk5Gbfccot3G5PJBI/HgxMnTsBoNKKqqgpLlixBYWEhqqur4Xa70dzcjLKyMp86RowY0WbNkyZNwsiRI/HOO+9AqVQCAJqamlBaWor58+djwYIF3m1dLhciIyMBACUlJcjIyIBWq/WpjYIXgykREZGMhIeHo2/fvlddHxIS4v1eEISrLvN4PO0+Zk5ODmpra/GHP/wBKSkp0Gg0MJlMcDgcV9TWlunTp+O9997DsWPHvCG5sbERAPCnP/0Jo0aN8tn+Ungl+iEGUyIiogBXVlaGiooKJCYmAgD27t0LhUKBAQMGAAB2796N1157DdOmTQMAlJeX48KFC+3e/wsvvACdTocJEyagsLAQ6enpiI+PR2JiIr777jvMnj27zcelpaXhL3/5C2w2m7fVdO/evTfzVMnPMZgSERHJiN1uh9ls9lmmUqkQExPT4X1qtVrk5OTgxRdfhNVqxeOPP4777rsPRqMRANCvXz/85S9/wYgRI2C1WvHUU08hNDT0ho7x4osvwu12Y/z48SgsLERqaiqWL1+Oxx9/HJGRkZgyZQrsdjv279+PixcvIi8vDw8++CB+9atfYcGCBcjPz8fZs2fx4osvdvh5kv/jqHwiIiIZ2bJlCxISEnxud955503ts2/fvpg1axamTZuGyZMnIyMjw2fapjfeeAMXL17E8OHDMWfOHDz++OOIi4u74eO89NJLuO+++zB+/HicPHkS//7v/44///nPWLt2LQYPHoy77roL69atQ69evQAAOp0OH330EY4cOYJhw4bhV7/6FX7729/e1HMl/yaIoihKXQQREREREVtMiYiIiEgWGEyJiIiISBYYTImIiIhIFhhMiYiIiEgWGEyJiIiISBYYTImIiIhIFhhMiYiIiEgWGEyJiIiISBYYTImIiIhIFhhMiYiIiEgWGEyJiIiISBYYTImIiIhIFv4/BxNgS5sQ83cAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 700x350 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "figure, axes = plt.subplots(1, 2)\n",
    "embarked_count = cleaned_titanic_train['Embarked'].value_counts()\n",
    "embarked_label = embarked_count.index\n",
    "axes[0].pie(embarked_count, labels=embarked_label)\n",
    "sns.countplot(cleaned_titanic_train, x='Embarked', hue='Survived', ax=axes[1])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从是否幸存与登船港口之间的柱状图来看，瑟堡登船的乘客，幸存数量大于遇难数量，而皇后镇和南安普敦则相反。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 家庭成员数量与是否幸存的关系"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAqcAAAFUCAYAAAAZC5UuAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8g+/7EAAAACXBIWXMAAA9hAAAPYQGoP6dpAABiM0lEQVR4nO3deXxU9b3/8deZPXtISDKJrLKDbIJg3IqILKLXBddSxaX6uBRskbZa7s+leq1Ye9tavV5Qr4pWuVptQYuKIgoosluURZBVgmQP2ZNZz++PwEhkyzozSd7Px2MeMmfOnPOZmJl55/v9nu/XME3TREREREQkClgiXYCIiIiIyFEKpyIiIiISNRRORURERCRqKJyKiIiISNRQOBURERGRqKFwKiIiIiJRQ+FURERERKKGwqmIiIiIRA1bpAsQEZHmCQaDHDp0iISEBAzDiHQ5IiLHMU2TiooKsrKysFhO3TaqcCoi0sYdOnSIrl27RroMEZHTysnJoUuXLqfcR+FURKSNS0hIAOo+9BMTEyNcjYjI8crLy+natWvo8+pUFE5FRNq4o135iYmJCqciEtUaMvRIF0SJiIiISNRQOBURERGRqKFwKiIiIiJRQ2NORURERBopEAjg8/kiXUbUsNvtWK3WFjmWwqmIiIhIA5mmSV5eHqWlpZEuJeokJyfjdrubPd+ywqmIiIhIAx0Npunp6cTGxmrhC+oCe3V1NQUFBQBkZmY263gKpyIiIiINEAgEQsE0NTU10uVElZiYGAAKCgpIT09vVhe/LogSERERaYCjY0xjY2MjXEl0Ovpzae5YXIVTERERkUZQV/6JtdTPReFURERERKKGxpyKiLQzb60vbPRzrh2V1gqViEi4rFixgosvvpjDhw+TnJzcaue59dZbKS0tZfHixa12DrWcioiIiLSQwsJCpk+fTrdu3XA6nbjdbiZMmMDq1atb9bznnXceubm5JCUltep5wkEtpyIiIiItZMqUKXi9Xl5++WXOPPNM8vPzWb58OcXFxU06nmmaBAIBbLZTRzaHw4Hb7W7SOaKNWk5FREREWkBpaSmffvopv//977n44ovp3r07o0aNYs6cOfzbv/0b+/fvxzAMNm/eXO85hmGwYsUKoK573jAM3n//fUaMGIHT6eTFF1/EMAx27NhR73x//vOf6dWrV73nlZaWUl5eTkxMDO+//369/RctWkRCQgLV1dUA5OTkcP3115OcnExKSgpXXnkl+/fvD+0fCASYPXs2ycnJpKamcu+992KaZsv/4H5A4TTKPfPMM/To0QOXy8Xo0aNZv359pEsSERGRE4iPjyc+Pp7Fixfj8Xiadazf/OY3PP7443z99ddce+21jBw5ktdee63ePq+99ho//vGPj3tuYmIil19+OQsXLjxu/6uuuorY2Fh8Ph8TJkwgISGBTz/9lNWrVxMfH8/EiRPxer0A/PGPf2TBggW8+OKLfPbZZ5SUlLBo0aJmva6GUDiNYm+88QazZ8/moYce4osvvmDo0KFMmDAhtAKDiIiIRA+bzcaCBQt4+eWXSU5O5vzzz+c//uM/+Oqrrxp9rEceeYRLL72UXr16kZKSwtSpU/m///u/0OPffPMNmzZtYurUqSd8/tSpU1m8eHGolbS8vJx33303tP8bb7xBMBjkf//3fxk8eDADBgzgpZde4sCBA6FW3CeffJI5c+ZwzTXXMGDAAObPnx+WMa0Kp1HsT3/6E3feeSe33XYbAwcOZP78+cTGxvLiiy9GujQRERE5gSlTpnDo0CHeeecdJk6cyIoVKzj77LNZsGBBo44zcuTIevdvvPFG9u/fz9q1a4G6VtCzzz6b/v37n/D5l112GXa7nXfeeQeAv//97yQmJjJu3DgAvvzyS3bv3k1CQkKoxTclJYXa2lr27NlDWVkZubm5jB49OnRMm812XF2tQeE0Snm9XjZt2hT6JQKwWCyMGzeONWvWRLAyERERORWXy8Wll17KAw88wOeff86tt97KQw89hMVSF7uOHbd5stWU4uLi6t13u92MHTs21FW/cOHCk7aaQt0FUtdee229/W+44YbQhVWVlZWMGDGCzZs317t98803JxwqEE4Kp1GqqKiIQCBARkZGve0ZGRnk5eVFqCoRERFprIEDB1JVVUVaWt18wrm5uaHHjr046nSmTp3KG2+8wZo1a9i7dy833njjafdfunQp27Zt4+OPP64XZs8++2x27dpFeno6vXv3rndLSkoiKSmJzMxM1q1bF3qO3+9n06ZNDa63qRRORURERFpAcXExY8eO5dVXX+Wrr75i3759vPnmmzzxxBNceeWVxMTEcO6554YudFq5ciX3339/g49/zTXXUFFRwfTp07n44ovJyso65f4XXXQRbrebqVOn0rNn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X817773He++9x1//+leeffZZ3nrrrQad86c//SkLFy7E4/GEtr366qucccYZjB07NrQtMTGR//f//h+PPPIIVVVVzXqdL7/8Mp07d2b9+vXcfffdTJ8+neuuu47zzjuPL774gvHjx3PzzTdTXV3drPNI26BwKiIiEgWWLFlCfHx86Hbdddcxa9YsLr74Ynr06MHYsWN59NFH+dvf/lbveT6fj3nz5jF8+HAuuugirr32Wj777DNeeOEFBg4cyOWXX87FF1/MJ5980qA6rrnmGgDefvvt0LYFCxaExsUe62c/+xkul4s//elPzXrtQ4cO5f7776dPnz7MmTMHl8tF586dufPOO+nTpw8PPvggxcXFfPXVV806j7QNtkgXICIiInDxxRczb9680P24uDg++ugj5s6dy44dOygvL8fv91NbW0t1dXVozGhsbCy9evUKPS8jI4MePXoQHx9fb1tBQUGD6nC5XNx88828+OKLXH/99XzxxRds3bqVd95557h9nU4njzzySKi1s6mGDBkS+rfVaiU1NZXBgwfXqx9o8GuQtk0tpyIiIlEgLi6O3r17h24ej4fLL7+cIUOG8Pe//51NmzbxzDPPAOD1ekPPs9vt9Y5jGMYJtwWDwQbX8tOf/pRly5Zx8OBBXnrpJcaOHUv37t1PuO9PfvITunfvzqOPPnrcYxaLBdM062070QVUp3sNR1tsG/MapO1SOBUREYlCmzZtIhgM8sc//pFzzz2Xvn37cujQobCce/DgwYwcOZLnn3+ehQsXcvvtt590X4vFwty5c5k3bx779++v91haWhq5ubn1tm3evLkVKpb2ROFUREQkCvXu3Rufz8fTTz/N3r17+etf/8r8+fPDdv6f/vSnPP7445imydVXX33KfSdPnszo0aN59tln620fO3YsGzdu5JVXXmHXrl089NBDbN26tTXLlnZA4VRERCQKDR06lD/96U/8/ve/56yzzuK1115j7ty5YTv/TTfdhM1m46abbsLlcp12/9///vfU1tbW2zZhwgQeeOAB7r33Xs455xwqKiq45ZZbWqtkaScM84eDQURERKTD279/P7169WLDhg2cffbZkS5HOhCFUxEREQnx+XwUFxfzq1/9in379rF69epIlyQdjLr1RUREJGT16tVkZmayYcOGsI5xFTlKLaciIiIiEjXUcioiIiIiUUPhVERERESihsKpiIiIiEQNhVMRERERiRoKpyIiIiISNRRORURERCRqKJyKiIiISNRQOBURERGRqKFwKiIiIiJR4/8DRC6OUt++4iMAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 700x350 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "figure, axes = plt.subplots(1, 2)\n",
    "familyNum_count = cleaned_titanic_train['FamilyNum'].value_counts()\n",
    "familyNum_label = familyNum_count.index\n",
    "axes[0].pie(familyNum_count, labels=familyNum_label)\n",
    "sns.countplot(cleaned_titanic_train, x='FamilyNum', hue='Survived', ax=axes[1])\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从是否幸存与乘客家庭成员之间的柱状图来看，独身的乘客中遇难的多于幸存的。从有携带家庭成员的乘客来看，家庭成员在1～3位之间的幸存人数超过遇难人数，但同乘家庭成员超过3位后，遇难的更多。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 891 entries, 0 to 890\n",
      "Data columns (total 13 columns):\n",
      " #   Column       Non-Null Count  Dtype   \n",
      "---  ------       --------------  -----   \n",
      " 0   PassengerId  891 non-null    object  \n",
      " 1   Survived     891 non-null    category\n",
      " 2   Pclass       891 non-null    category\n",
      " 3   Name         891 non-null    object  \n",
      " 4   Sex          891 non-null    category\n",
      " 5   Age          891 non-null    float64 \n",
      " 6   SibSp        891 non-null    int64   \n",
      " 7   Parch        891 non-null    int64   \n",
      " 8   Ticket       891 non-null    object  \n",
      " 9   Fare         891 non-null    float64 \n",
      " 10  Cabin        204 non-null    object  \n",
      " 11  Embarked     889 non-null    category\n",
      " 12  FamilyNum    891 non-null    int64   \n",
      "dtypes: category(4), float64(2), int64(3), object(4)\n",
      "memory usage: 66.8+ KB\n"
     ]
    }
   ],
   "source": [
    "cleaned_titanic_train.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 分析数据"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "在分析步骤中，我们将利用以上清理后到的数据，进行逻辑回归分析，目标是得到一个可以根据泰坦尼克号乘客各个属性，对沉船事件后幸存情况进行预测的数学模型。\n",
    "\n",
    "我们先引入做逻辑回归所需的模块。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [],
   "source": [
    "import statsmodels.api as sm"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "然后可以创建一个新的DataFrame`lr_titanic_train`，让它作为我们进逻辑性回归分析所用的数据。\n",
    "\n",
    "和`cleaned_titanic_train`区分开的原因是，我们在进行回归分析前，还可能需要对数据进行一些准备，比如引入虚拟变量，这些都可以在`lr_titanic_train`上执行。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "      <th>FamilyNum</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Braund, Mr. Owen Harris</td>\n",
       "      <td>male</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>A/5 21171</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>\n",
       "      <td>female</td>\n",
       "      <td>38.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>PC 17599</td>\n",
       "      <td>71.2833</td>\n",
       "      <td>C85</td>\n",
       "      <td>C</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>Heikkinen, Miss. Laina</td>\n",
       "      <td>female</td>\n",
       "      <td>26.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>STON/O2. 3101282</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>\n",
       "      <td>female</td>\n",
       "      <td>35.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>113803</td>\n",
       "      <td>53.1000</td>\n",
       "      <td>C123</td>\n",
       "      <td>S</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>Allen, Mr. William Henry</td>\n",
       "      <td>male</td>\n",
       "      <td>35.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>373450</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  PassengerId Survived Pclass  \\\n",
       "0           1        0      3   \n",
       "1           2        1      1   \n",
       "2           3        1      3   \n",
       "3           4        1      1   \n",
       "4           5        0      3   \n",
       "\n",
       "                                                Name     Sex   Age  SibSp  \\\n",
       "0                            Braund, Mr. Owen Harris    male  22.0      1   \n",
       "1  Cumings, Mrs. John Bradley (Florence Briggs Th...  female  38.0      1   \n",
       "2                             Heikkinen, Miss. Laina  female  26.0      0   \n",
       "3       Futrelle, Mrs. Jacques Heath (Lily May Peel)  female  35.0      1   \n",
       "4                           Allen, Mr. William Henry    male  35.0      0   \n",
       "\n",
       "   Parch            Ticket     Fare Cabin Embarked  FamilyNum  \n",
       "0      0         A/5 21171   7.2500   NaN        S          1  \n",
       "1      0          PC 17599  71.2833   C85        C          1  \n",
       "2      0  STON/O2. 3101282   7.9250   NaN        S          0  \n",
       "3      0            113803  53.1000  C123        S          1  \n",
       "4      0            373450   8.0500   NaN        S          0  "
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr_titanic_train = cleaned_titanic_train.copy()\n",
    "lr_titanic_train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "移除大概率不会影响乘客幸存概率的变量。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Survived</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Fare</th>\n",
       "      <th>FamilyNum</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>male</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>female</td>\n",
       "      <td>38.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>71.2833</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1</td>\n",
       "      <td>3</td>\n",
       "      <td>female</td>\n",
       "      <td>26.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>female</td>\n",
       "      <td>35.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>53.1000</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0</td>\n",
       "      <td>3</td>\n",
       "      <td>male</td>\n",
       "      <td>35.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Survived Pclass     Sex   Age  SibSp  Parch     Fare  FamilyNum\n",
       "0        0      3    male  22.0      1      0   7.2500          1\n",
       "1        1      1  female  38.0      1      0  71.2833          1\n",
       "2        1      3  female  26.0      0      0   7.9250          0\n",
       "3        1      1  female  35.0      1      0  53.1000          1\n",
       "4        0      3    male  35.0      0      0   8.0500          0"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr_titanic_train = lr_titanic_train.drop(['PassengerId', 'Name', 'Ticket', 'Cabin', 'Embarked'], axis=1)\n",
    "lr_titanic_train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "数据里还存在分类变量，无法直接建立逻辑回归模型。我们需要引入虚拟变量，也就是用0和1分别表示是否属于该类别。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Survived</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Fare</th>\n",
       "      <th>FamilyNum</th>\n",
       "      <th>Pclass_2</th>\n",
       "      <th>Pclass_3</th>\n",
       "      <th>Sex_male</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>7.2500</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>38.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>71.2833</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1</td>\n",
       "      <td>26.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>7.9250</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1</td>\n",
       "      <td>35.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>53.1000</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0</td>\n",
       "      <td>35.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>8.0500</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Survived   Age  SibSp  Parch     Fare  FamilyNum  Pclass_2  Pclass_3  \\\n",
       "0        0  22.0      1      0   7.2500          1         0         1   \n",
       "1        1  38.0      1      0  71.2833          1         0         0   \n",
       "2        1  26.0      0      0   7.9250          0         0         1   \n",
       "3        1  35.0      1      0  53.1000          1         0         0   \n",
       "4        0  35.0      0      0   8.0500          0         0         1   \n",
       "\n",
       "   Sex_male  \n",
       "0         1  \n",
       "1         0  \n",
       "2         0  \n",
       "3         0  \n",
       "4         1  "
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr_titanic_train = pd.get_dummies(lr_titanic_train, drop_first=True, columns=['Pclass', 'Sex'], dtype=int)\n",
    "lr_titanic_train.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "接下来，我们要把因变量和自变量划分出来。\n",
    "\n",
    "因变量是`Survived`变量，因为我们进行逻辑回归的目的，是根据其它可能对乘客生还概率有影响的变量，来预测幸存情况。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [],
   "source": [
    "y = lr_titanic_train['Survived']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "我们可以把除`Survived`之外的先纳入自变量，但需要查看它们之间的相关性。如果其中有些变量之间相关性很高，会导致共线性。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Fare</th>\n",
       "      <th>FamilyNum</th>\n",
       "      <th>Pclass_2</th>\n",
       "      <th>Pclass_3</th>\n",
       "      <th>Sex_male</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Age</th>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.232625</td>\n",
       "      <td>-0.179191</td>\n",
       "      <td>0.091566</td>\n",
       "      <td>-0.248512</td>\n",
       "      <td>0.006589</td>\n",
       "      <td>-0.281004</td>\n",
       "      <td>0.084153</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>SibSp</th>\n",
       "      <td>-0.232625</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.414838</td>\n",
       "      <td>0.159651</td>\n",
       "      <td>0.890712</td>\n",
       "      <td>-0.055932</td>\n",
       "      <td>0.092548</td>\n",
       "      <td>-0.114631</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Parch</th>\n",
       "      <td>-0.179191</td>\n",
       "      <td>0.414838</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.216225</td>\n",
       "      <td>0.783111</td>\n",
       "      <td>-0.000734</td>\n",
       "      <td>0.015790</td>\n",
       "      <td>-0.245489</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Fare</th>\n",
       "      <td>0.091566</td>\n",
       "      <td>0.159651</td>\n",
       "      <td>0.216225</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.217138</td>\n",
       "      <td>-0.118557</td>\n",
       "      <td>-0.413333</td>\n",
       "      <td>-0.182333</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>FamilyNum</th>\n",
       "      <td>-0.248512</td>\n",
       "      <td>0.890712</td>\n",
       "      <td>0.783111</td>\n",
       "      <td>0.217138</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.038594</td>\n",
       "      <td>0.071142</td>\n",
       "      <td>-0.200988</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Pclass_2</th>\n",
       "      <td>0.006589</td>\n",
       "      <td>-0.055932</td>\n",
       "      <td>-0.000734</td>\n",
       "      <td>-0.118557</td>\n",
       "      <td>-0.038594</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.565210</td>\n",
       "      <td>-0.064746</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Pclass_3</th>\n",
       "      <td>-0.281004</td>\n",
       "      <td>0.092548</td>\n",
       "      <td>0.015790</td>\n",
       "      <td>-0.413333</td>\n",
       "      <td>0.071142</td>\n",
       "      <td>-0.565210</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.137143</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Sex_male</th>\n",
       "      <td>0.084153</td>\n",
       "      <td>-0.114631</td>\n",
       "      <td>-0.245489</td>\n",
       "      <td>-0.182333</td>\n",
       "      <td>-0.200988</td>\n",
       "      <td>-0.064746</td>\n",
       "      <td>0.137143</td>\n",
       "      <td>1.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                Age     SibSp     Parch      Fare  FamilyNum  Pclass_2  \\\n",
       "Age        1.000000 -0.232625 -0.179191  0.091566  -0.248512  0.006589   \n",
       "SibSp     -0.232625  1.000000  0.414838  0.159651   0.890712 -0.055932   \n",
       "Parch     -0.179191  0.414838  1.000000  0.216225   0.783111 -0.000734   \n",
       "Fare       0.091566  0.159651  0.216225  1.000000   0.217138 -0.118557   \n",
       "FamilyNum -0.248512  0.890712  0.783111  0.217138   1.000000 -0.038594   \n",
       "Pclass_2   0.006589 -0.055932 -0.000734 -0.118557  -0.038594  1.000000   \n",
       "Pclass_3  -0.281004  0.092548  0.015790 -0.413333   0.071142 -0.565210   \n",
       "Sex_male   0.084153 -0.114631 -0.245489 -0.182333  -0.200988 -0.064746   \n",
       "\n",
       "           Pclass_3  Sex_male  \n",
       "Age       -0.281004  0.084153  \n",
       "SibSp      0.092548 -0.114631  \n",
       "Parch      0.015790 -0.245489  \n",
       "Fare      -0.413333 -0.182333  \n",
       "FamilyNum  0.071142 -0.200988  \n",
       "Pclass_2  -0.565210 -0.064746  \n",
       "Pclass_3   1.000000  0.137143  \n",
       "Sex_male   0.137143  1.000000  "
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X = lr_titanic_train.drop(['Survived'], axis=1)\n",
    "X.corr()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "一般我们认为，当相关系数的绝对值大于0.8的时候，可能导致严重共线性，所以我们检查的时候，找绝对值大于0.8的值即可。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Fare</th>\n",
       "      <th>FamilyNum</th>\n",
       "      <th>Pclass_2</th>\n",
       "      <th>Pclass_3</th>\n",
       "      <th>Sex_male</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Age</th>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>SibSp</th>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Parch</th>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Fare</th>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>FamilyNum</th>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Pclass_2</th>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Pclass_3</th>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "      <td>False</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Sex_male</th>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>False</td>\n",
       "      <td>True</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "             Age  SibSp  Parch   Fare  FamilyNum  Pclass_2  Pclass_3  Sex_male\n",
       "Age         True  False  False  False      False     False     False     False\n",
       "SibSp      False   True  False  False       True     False     False     False\n",
       "Parch      False  False   True  False      False     False     False     False\n",
       "Fare       False  False  False   True      False     False     False     False\n",
       "FamilyNum  False   True  False  False       True     False     False     False\n",
       "Pclass_2   False  False  False  False      False      True     False     False\n",
       "Pclass_3   False  False  False  False      False     False      True     False\n",
       "Sex_male   False  False  False  False      False     False     False      True"
      ]
     },
     "execution_count": 38,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X.corr().abs() > 0.8"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从以上输出来看，`SibSp`和`FamilyNum`之间的相关系数绝对值大于0.8。这符合预期，因为`FamilyNum`是根据`SibSp`和`Parch`计算出来的。\n",
    "\n",
    "不同变量之间的如果相关性过高，会导致数值优化算法无法收敛，无法获得逻辑回归模型参数的计算结果，因此我们需要移除`FamilyNum`或`SibSp`。我们对同乘家庭成员是否会影响幸存概率感兴趣，所以保留`FamilyNum`。\n",
    "\n",
    "此外，如果仔细看相关系数数值，会发现`Parch`和`FamilyNum`之间也存在强相关，相关系数为0.78，接近0.8，因此我们也对`Parch`进行移除，避免算法无法收敛。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = X.drop(['Parch', 'SibSp'], axis=1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "接下来，给模型的线性方程添加截距。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [],
   "source": [
    "X = sm.add_constant(X)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "下一步就可以调用`Logit`函数，利用最大似然优化来得到逻辑回归模型的参数值，并输出总结信息。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Optimization terminated successfully.\n",
      "         Current function value: 0.443547\n",
      "         Iterations 6\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table class=\"simpletable\">\n",
       "<caption>Logit Regression Results</caption>\n",
       "<tr>\n",
       "  <th>Dep. Variable:</th>       <td>Survived</td>     <th>  No. Observations:  </th>  <td>   891</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Model:</th>                 <td>Logit</td>      <th>  Df Residuals:      </th>  <td>   884</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Method:</th>                 <td>MLE</td>       <th>  Df Model:          </th>  <td>     6</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Date:</th>            <td>Sat, 09 Dec 2023</td> <th>  Pseudo R-squ.:     </th>  <td>0.3339</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Time:</th>                <td>14:37:29</td>     <th>  Log-Likelihood:    </th> <td> -395.20</td> \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>converged:</th>             <td>True</td>       <th>  LL-Null:           </th> <td> -593.33</td> \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Covariance Type:</th>     <td>nonrobust</td>    <th>  LLR p-value:       </th> <td>1.786e-82</td>\n",
       "</tr>\n",
       "</table>\n",
       "<table class=\"simpletable\">\n",
       "<tr>\n",
       "      <td></td>         <th>coef</th>     <th>std err</th>      <th>z</th>      <th>P>|z|</th>  <th>[0.025</th>    <th>0.975]</th>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>const</th>     <td>    3.8097</td> <td>    0.445</td> <td>    8.568</td> <td> 0.000</td> <td>    2.938</td> <td>    4.681</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Age</th>       <td>   -0.0388</td> <td>    0.008</td> <td>   -4.963</td> <td> 0.000</td> <td>   -0.054</td> <td>   -0.023</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Fare</th>      <td>    0.0032</td> <td>    0.002</td> <td>    1.311</td> <td> 0.190</td> <td>   -0.002</td> <td>    0.008</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>FamilyNum</th> <td>   -0.2430</td> <td>    0.068</td> <td>   -3.594</td> <td> 0.000</td> <td>   -0.376</td> <td>   -0.110</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Pclass_2</th>  <td>   -1.0003</td> <td>    0.293</td> <td>   -3.416</td> <td> 0.001</td> <td>   -1.574</td> <td>   -0.426</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Pclass_3</th>  <td>   -2.1324</td> <td>    0.289</td> <td>   -7.373</td> <td> 0.000</td> <td>   -2.699</td> <td>   -1.566</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Sex_male</th>  <td>   -2.7759</td> <td>    0.199</td> <td>  -13.980</td> <td> 0.000</td> <td>   -3.165</td> <td>   -2.387</td>\n",
       "</tr>\n",
       "</table>"
      ],
      "text/latex": [
       "\\begin{center}\n",
       "\\begin{tabular}{lclc}\n",
       "\\toprule\n",
       "\\textbf{Dep. Variable:}   &     Survived     & \\textbf{  No. Observations:  } &      891    \\\\\n",
       "\\textbf{Model:}           &      Logit       & \\textbf{  Df Residuals:      } &      884    \\\\\n",
       "\\textbf{Method:}          &       MLE        & \\textbf{  Df Model:          } &        6    \\\\\n",
       "\\textbf{Date:}            & Sat, 09 Dec 2023 & \\textbf{  Pseudo R-squ.:     } &   0.3339    \\\\\n",
       "\\textbf{Time:}            &     14:37:29     & \\textbf{  Log-Likelihood:    } &   -395.20   \\\\\n",
       "\\textbf{converged:}       &       True       & \\textbf{  LL-Null:           } &   -593.33   \\\\\n",
       "\\textbf{Covariance Type:} &    nonrobust     & \\textbf{  LLR p-value:       } & 1.786e-82   \\\\\n",
       "\\bottomrule\n",
       "\\end{tabular}\n",
       "\\begin{tabular}{lcccccc}\n",
       "                   & \\textbf{coef} & \\textbf{std err} & \\textbf{z} & \\textbf{P$> |$z$|$} & \\textbf{[0.025} & \\textbf{0.975]}  \\\\\n",
       "\\midrule\n",
       "\\textbf{const}     &       3.8097  &        0.445     &     8.568  &         0.000        &        2.938    &        4.681     \\\\\n",
       "\\textbf{Age}       &      -0.0388  &        0.008     &    -4.963  &         0.000        &       -0.054    &       -0.023     \\\\\n",
       "\\textbf{Fare}      &       0.0032  &        0.002     &     1.311  &         0.190        &       -0.002    &        0.008     \\\\\n",
       "\\textbf{FamilyNum} &      -0.2430  &        0.068     &    -3.594  &         0.000        &       -0.376    &       -0.110     \\\\\n",
       "\\textbf{Pclass\\_2} &      -1.0003  &        0.293     &    -3.416  &         0.001        &       -1.574    &       -0.426     \\\\\n",
       "\\textbf{Pclass\\_3} &      -2.1324  &        0.289     &    -7.373  &         0.000        &       -2.699    &       -1.566     \\\\\n",
       "\\textbf{Sex\\_male} &      -2.7759  &        0.199     &   -13.980  &         0.000        &       -3.165    &       -2.387     \\\\\n",
       "\\bottomrule\n",
       "\\end{tabular}\n",
       "%\\caption{Logit Regression Results}\n",
       "\\end{center}"
      ],
      "text/plain": [
       "<class 'statsmodels.iolib.summary.Summary'>\n",
       "\"\"\"\n",
       "                           Logit Regression Results                           \n",
       "==============================================================================\n",
       "Dep. Variable:               Survived   No. Observations:                  891\n",
       "Model:                          Logit   Df Residuals:                      884\n",
       "Method:                           MLE   Df Model:                            6\n",
       "Date:                Sat, 09 Dec 2023   Pseudo R-squ.:                  0.3339\n",
       "Time:                        14:37:29   Log-Likelihood:                -395.20\n",
       "converged:                       True   LL-Null:                       -593.33\n",
       "Covariance Type:            nonrobust   LLR p-value:                 1.786e-82\n",
       "==============================================================================\n",
       "                 coef    std err          z      P>|z|      [0.025      0.975]\n",
       "------------------------------------------------------------------------------\n",
       "const          3.8097      0.445      8.568      0.000       2.938       4.681\n",
       "Age           -0.0388      0.008     -4.963      0.000      -0.054      -0.023\n",
       "Fare           0.0032      0.002      1.311      0.190      -0.002       0.008\n",
       "FamilyNum     -0.2430      0.068     -3.594      0.000      -0.376      -0.110\n",
       "Pclass_2      -1.0003      0.293     -3.416      0.001      -1.574      -0.426\n",
       "Pclass_3      -2.1324      0.289     -7.373      0.000      -2.699      -1.566\n",
       "Sex_male      -2.7759      0.199    -13.980      0.000      -3.165      -2.387\n",
       "==============================================================================\n",
       "\"\"\""
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model = sm.Logit(y, X).fit()\n",
    "model.summary()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "当我们把显著区间设定为0.05时，以上结果的P值可以看出，模型认为船票价格对乘客幸存概率没有显著性影响。因此可以把这个变量移除后，再次建立逻辑回归模型。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Optimization terminated successfully.\n",
      "         Current function value: 0.444623\n",
      "         Iterations 6\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<table class=\"simpletable\">\n",
       "<caption>Logit Regression Results</caption>\n",
       "<tr>\n",
       "  <th>Dep. Variable:</th>       <td>Survived</td>     <th>  No. Observations:  </th>  <td>   891</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Model:</th>                 <td>Logit</td>      <th>  Df Residuals:      </th>  <td>   885</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Method:</th>                 <td>MLE</td>       <th>  Df Model:          </th>  <td>     5</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Date:</th>            <td>Sat, 09 Dec 2023</td> <th>  Pseudo R-squ.:     </th>  <td>0.3323</td>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Time:</th>                <td>14:37:29</td>     <th>  Log-Likelihood:    </th> <td> -396.16</td> \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>converged:</th>             <td>True</td>       <th>  LL-Null:           </th> <td> -593.33</td> \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Covariance Type:</th>     <td>nonrobust</td>    <th>  LLR p-value:       </th> <td>4.927e-83</td>\n",
       "</tr>\n",
       "</table>\n",
       "<table class=\"simpletable\">\n",
       "<tr>\n",
       "      <td></td>         <th>coef</th>     <th>std err</th>      <th>z</th>      <th>P>|z|</th>  <th>[0.025</th>    <th>0.975]</th>  \n",
       "</tr>\n",
       "<tr>\n",
       "  <th>const</th>     <td>    4.0620</td> <td>    0.404</td> <td>   10.049</td> <td> 0.000</td> <td>    3.270</td> <td>    4.854</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Age</th>       <td>   -0.0395</td> <td>    0.008</td> <td>   -5.065</td> <td> 0.000</td> <td>   -0.055</td> <td>   -0.024</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>FamilyNum</th> <td>   -0.2186</td> <td>    0.065</td> <td>   -3.383</td> <td> 0.001</td> <td>   -0.345</td> <td>   -0.092</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Pclass_2</th>  <td>   -1.1798</td> <td>    0.261</td> <td>   -4.518</td> <td> 0.000</td> <td>   -1.692</td> <td>   -0.668</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Pclass_3</th>  <td>   -2.3458</td> <td>    0.242</td> <td>   -9.676</td> <td> 0.000</td> <td>   -2.821</td> <td>   -1.871</td>\n",
       "</tr>\n",
       "<tr>\n",
       "  <th>Sex_male</th>  <td>   -2.7854</td> <td>    0.198</td> <td>  -14.069</td> <td> 0.000</td> <td>   -3.173</td> <td>   -2.397</td>\n",
       "</tr>\n",
       "</table>"
      ],
      "text/latex": [
       "\\begin{center}\n",
       "\\begin{tabular}{lclc}\n",
       "\\toprule\n",
       "\\textbf{Dep. Variable:}   &     Survived     & \\textbf{  No. Observations:  } &      891    \\\\\n",
       "\\textbf{Model:}           &      Logit       & \\textbf{  Df Residuals:      } &      885    \\\\\n",
       "\\textbf{Method:}          &       MLE        & \\textbf{  Df Model:          } &        5    \\\\\n",
       "\\textbf{Date:}            & Sat, 09 Dec 2023 & \\textbf{  Pseudo R-squ.:     } &   0.3323    \\\\\n",
       "\\textbf{Time:}            &     14:37:29     & \\textbf{  Log-Likelihood:    } &   -396.16   \\\\\n",
       "\\textbf{converged:}       &       True       & \\textbf{  LL-Null:           } &   -593.33   \\\\\n",
       "\\textbf{Covariance Type:} &    nonrobust     & \\textbf{  LLR p-value:       } & 4.927e-83   \\\\\n",
       "\\bottomrule\n",
       "\\end{tabular}\n",
       "\\begin{tabular}{lcccccc}\n",
       "                   & \\textbf{coef} & \\textbf{std err} & \\textbf{z} & \\textbf{P$> |$z$|$} & \\textbf{[0.025} & \\textbf{0.975]}  \\\\\n",
       "\\midrule\n",
       "\\textbf{const}     &       4.0620  &        0.404     &    10.049  &         0.000        &        3.270    &        4.854     \\\\\n",
       "\\textbf{Age}       &      -0.0395  &        0.008     &    -5.065  &         0.000        &       -0.055    &       -0.024     \\\\\n",
       "\\textbf{FamilyNum} &      -0.2186  &        0.065     &    -3.383  &         0.001        &       -0.345    &       -0.092     \\\\\n",
       "\\textbf{Pclass\\_2} &      -1.1798  &        0.261     &    -4.518  &         0.000        &       -1.692    &       -0.668     \\\\\n",
       "\\textbf{Pclass\\_3} &      -2.3458  &        0.242     &    -9.676  &         0.000        &       -2.821    &       -1.871     \\\\\n",
       "\\textbf{Sex\\_male} &      -2.7854  &        0.198     &   -14.069  &         0.000        &       -3.173    &       -2.397     \\\\\n",
       "\\bottomrule\n",
       "\\end{tabular}\n",
       "%\\caption{Logit Regression Results}\n",
       "\\end{center}"
      ],
      "text/plain": [
       "<class 'statsmodels.iolib.summary.Summary'>\n",
       "\"\"\"\n",
       "                           Logit Regression Results                           \n",
       "==============================================================================\n",
       "Dep. Variable:               Survived   No. Observations:                  891\n",
       "Model:                          Logit   Df Residuals:                      885\n",
       "Method:                           MLE   Df Model:                            5\n",
       "Date:                Sat, 09 Dec 2023   Pseudo R-squ.:                  0.3323\n",
       "Time:                        14:37:29   Log-Likelihood:                -396.16\n",
       "converged:                       True   LL-Null:                       -593.33\n",
       "Covariance Type:            nonrobust   LLR p-value:                 4.927e-83\n",
       "==============================================================================\n",
       "                 coef    std err          z      P>|z|      [0.025      0.975]\n",
       "------------------------------------------------------------------------------\n",
       "const          4.0620      0.404     10.049      0.000       3.270       4.854\n",
       "Age           -0.0395      0.008     -5.065      0.000      -0.055      -0.024\n",
       "FamilyNum     -0.2186      0.065     -3.383      0.001      -0.345      -0.092\n",
       "Pclass_2      -1.1798      0.261     -4.518      0.000      -1.692      -0.668\n",
       "Pclass_3      -2.3458      0.242     -9.676      0.000      -2.821      -1.871\n",
       "Sex_male      -2.7854      0.198    -14.069      0.000      -3.173      -2.397\n",
       "==============================================================================\n",
       "\"\"\""
      ]
     },
     "execution_count": 42,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X = X.drop(['Fare'], axis=1)\n",
    "model = sm.Logit(y, X).fit()\n",
    "model.summary()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "逻辑回归模型预测以下因素的增加（或存在）会降低幸存概率：年龄、同乘家庭成员数、不在一等舱、性别为男性。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "要理解各个各个自变量系数的实际含义，我们需要计算自然常数的次方。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.9612699539905982"
      ]
     },
     "execution_count": 43,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Age\n",
    "np.exp(-0.0395)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "以上结果说明，年龄每增加1岁，生还概率降低4%左右。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.803643111115195"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# FamilyNum\n",
    "np.exp(-0.2186)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "以上结果说明，每多一名同乘家庭成员，生还概率降低20%左右。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.30734020049483596"
      ]
     },
     "execution_count": 45,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Pclass_2\n",
    "np.exp(-1.1798)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "以上结果说明，二等舱乘客的生还概率比一等舱乘客低71%左右。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.09577055503172162"
      ]
     },
     "execution_count": 46,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Pclass_3\n",
    "np.exp(-2.3458)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "以上结果说明，三等舱乘客的生还概率比一等舱乘客低90%左右。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.061704402333015156"
      ]
     },
     "execution_count": 47,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Sex_male\n",
    "np.exp(-2.7854)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "以上结果说明，男性乘客的生还概率比女性乘客低94%左右。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "根据模型参数值，我们总结：\n",
    "- 年龄小的乘客幸存概率更高；\n",
    "- 女性乘客的生还率比男性乘客的幸存概率更高；\n",
    "- 来自的船舱等级高的乘客幸存概率更高；\n",
    "- 同乘家庭成员少的乘客幸存概率更高。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "前两条背后的原因可能与泰坦尼克号沉船后逃生时，“让孩子和女性先走”的原则。第三条说明可能当时舱位更尊贵的乘客拥有了优先逃生的机会。第四条可能是因为拥有较大数量家庭成员的乘客在灾难发生时会急于解救其他家庭成员而非选择逃生，最后也失去了自己逃生的机会。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "得到模型后，我们将用于预测`titianic_test.csv`里泰坦尼克号乘客的生还情况。\n",
    "\n",
    "首先读取`titianic_test.csv`的数据。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Pclass</th>\n",
       "      <th>Name</th>\n",
       "      <th>Sex</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>892</td>\n",
       "      <td>3</td>\n",
       "      <td>Kelly, Mr. James</td>\n",
       "      <td>male</td>\n",
       "      <td>34.5</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330911</td>\n",
       "      <td>7.8292</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>893</td>\n",
       "      <td>3</td>\n",
       "      <td>Wilkes, Mrs. James (Ellen Needs)</td>\n",
       "      <td>female</td>\n",
       "      <td>47.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>363272</td>\n",
       "      <td>7.0000</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>894</td>\n",
       "      <td>2</td>\n",
       "      <td>Myles, Mr. Thomas Francis</td>\n",
       "      <td>male</td>\n",
       "      <td>62.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>240276</td>\n",
       "      <td>9.6875</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>895</td>\n",
       "      <td>3</td>\n",
       "      <td>Wirz, Mr. Albert</td>\n",
       "      <td>male</td>\n",
       "      <td>27.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>315154</td>\n",
       "      <td>8.6625</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>896</td>\n",
       "      <td>3</td>\n",
       "      <td>Hirvonen, Mrs. Alexander (Helga E Lindqvist)</td>\n",
       "      <td>female</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>3101298</td>\n",
       "      <td>12.2875</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   PassengerId  Pclass                                          Name     Sex  \\\n",
       "0          892       3                              Kelly, Mr. James    male   \n",
       "1          893       3              Wilkes, Mrs. James (Ellen Needs)  female   \n",
       "2          894       2                     Myles, Mr. Thomas Francis    male   \n",
       "3          895       3                              Wirz, Mr. Albert    male   \n",
       "4          896       3  Hirvonen, Mrs. Alexander (Helga E Lindqvist)  female   \n",
       "\n",
       "    Age  SibSp  Parch   Ticket     Fare Cabin Embarked  \n",
       "0  34.5      0      0   330911   7.8292   NaN        Q  \n",
       "1  47.0      1      0   363272   7.0000   NaN        S  \n",
       "2  62.0      0      0   240276   9.6875   NaN        Q  \n",
       "3  27.0      0      0   315154   8.6625   NaN        S  \n",
       "4  22.0      1      1  3101298  12.2875   NaN        S  "
      ]
     },
     "execution_count": 48,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "titanic_test = pd.read_csv(\"titanic_test.csv\")\n",
    "titanic_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "由于逻辑回归模型不允许数据中有缺失值，因此我们需要检查`titanic_test`是否存在数据缺失。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 418 entries, 0 to 417\n",
      "Data columns (total 11 columns):\n",
      " #   Column       Non-Null Count  Dtype  \n",
      "---  ------       --------------  -----  \n",
      " 0   PassengerId  418 non-null    int64  \n",
      " 1   Pclass       418 non-null    int64  \n",
      " 2   Name         418 non-null    object \n",
      " 3   Sex          418 non-null    object \n",
      " 4   Age          332 non-null    float64\n",
      " 5   SibSp        418 non-null    int64  \n",
      " 6   Parch        418 non-null    int64  \n",
      " 7   Ticket       418 non-null    object \n",
      " 8   Fare         417 non-null    float64\n",
      " 9   Cabin        91 non-null     object \n",
      " 10  Embarked     418 non-null    object \n",
      "dtypes: float64(2), int64(4), object(5)\n",
      "memory usage: 36.1+ KB\n"
     ]
    }
   ],
   "source": [
    "titanic_test.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "从以上输出可见，`Age`、`Fare`、`Cabin`存在缺失值。其中`Fare`和`Cabin`不属于回归模型的自变量，即使缺失也不会影响预测，因此可以忽略；`Age`需要我们进行和针对`cleaned_titanic_train`同样的操作，即用平均值填充。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 50,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "titanic_test['Age'] = titanic_test['Age'].fillna(titanic_test['Age'].mean())\n",
    "titanic_test['Age'].isna().sum()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "下一步是给模型中的分类变量引入虚拟变量，但在引入前我们需要先把分类变量的类型转换为Category，并且通过`categories`参数，让程序知道所有可能的分类值。这样做的原因是，预测数据包含的分类可能不全。我们需要确保引入虚拟变量的时候，不会漏掉某个或某些分类。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [],
   "source": [
    "titanic_test['Pclass'] = pd.Categorical(titanic_test['Pclass'], categories=['1', '2', '3'])\n",
    "titanic_test['Sex'] = pd.Categorical(titanic_test['Sex'], categories=['female', 'male'])\n",
    "titanic_test['Embarked'] = pd.Categorical(titanic_test['Embarked'], categories=['C', 'Q', 'S'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "下一步，给模型用到的分类变量引入虚拟变量。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Name</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "      <th>Pclass_2</th>\n",
       "      <th>Pclass_3</th>\n",
       "      <th>Sex_male</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>892</td>\n",
       "      <td>Kelly, Mr. James</td>\n",
       "      <td>34.5</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330911</td>\n",
       "      <td>7.8292</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>893</td>\n",
       "      <td>Wilkes, Mrs. James (Ellen Needs)</td>\n",
       "      <td>47.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>363272</td>\n",
       "      <td>7.0000</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>894</td>\n",
       "      <td>Myles, Mr. Thomas Francis</td>\n",
       "      <td>62.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>240276</td>\n",
       "      <td>9.6875</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>895</td>\n",
       "      <td>Wirz, Mr. Albert</td>\n",
       "      <td>27.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>315154</td>\n",
       "      <td>8.6625</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>896</td>\n",
       "      <td>Hirvonen, Mrs. Alexander (Helga E Lindqvist)</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>3101298</td>\n",
       "      <td>12.2875</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   PassengerId                                          Name   Age  SibSp  \\\n",
       "0          892                              Kelly, Mr. James  34.5      0   \n",
       "1          893              Wilkes, Mrs. James (Ellen Needs)  47.0      1   \n",
       "2          894                     Myles, Mr. Thomas Francis  62.0      0   \n",
       "3          895                              Wirz, Mr. Albert  27.0      0   \n",
       "4          896  Hirvonen, Mrs. Alexander (Helga E Lindqvist)  22.0      1   \n",
       "\n",
       "   Parch   Ticket     Fare Cabin Embarked  Pclass_2  Pclass_3  Sex_male  \n",
       "0      0   330911   7.8292   NaN        Q         0         0         1  \n",
       "1      0   363272   7.0000   NaN        S         0         0         0  \n",
       "2      0   240276   9.6875   NaN        Q         0         0         1  \n",
       "3      0   315154   8.6625   NaN        S         0         0         1  \n",
       "4      1  3101298  12.2875   NaN        S         0         0         0  "
      ]
     },
     "execution_count": 52,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "titanic_test = pd.get_dummies(titanic_test, drop_first=True, columns=['Pclass', 'Sex'], dtype=int)\n",
    "titanic_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "查看一下模型需要的输入变量。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "const        4.061982\n",
       "Age         -0.039495\n",
       "FamilyNum   -0.218627\n",
       "Pclass_2    -1.179763\n",
       "Pclass_3    -2.345823\n",
       "Sex_male    -2.785398\n",
       "dtype: float64"
      ]
     },
     "execution_count": 53,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.params"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "由于我们在数据整理步骤建立了`FamilyNum`变量，此处也需要对预测数据加上此变量。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>PassengerId</th>\n",
       "      <th>Name</th>\n",
       "      <th>Age</th>\n",
       "      <th>SibSp</th>\n",
       "      <th>Parch</th>\n",
       "      <th>Ticket</th>\n",
       "      <th>Fare</th>\n",
       "      <th>Cabin</th>\n",
       "      <th>Embarked</th>\n",
       "      <th>Pclass_2</th>\n",
       "      <th>Pclass_3</th>\n",
       "      <th>Sex_male</th>\n",
       "      <th>FamilyNum</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>892</td>\n",
       "      <td>Kelly, Mr. James</td>\n",
       "      <td>34.5</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>330911</td>\n",
       "      <td>7.8292</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>893</td>\n",
       "      <td>Wilkes, Mrs. James (Ellen Needs)</td>\n",
       "      <td>47.0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>363272</td>\n",
       "      <td>7.0000</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>894</td>\n",
       "      <td>Myles, Mr. Thomas Francis</td>\n",
       "      <td>62.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>240276</td>\n",
       "      <td>9.6875</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Q</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>895</td>\n",
       "      <td>Wirz, Mr. Albert</td>\n",
       "      <td>27.0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>315154</td>\n",
       "      <td>8.6625</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>896</td>\n",
       "      <td>Hirvonen, Mrs. Alexander (Helga E Lindqvist)</td>\n",
       "      <td>22.0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>3101298</td>\n",
       "      <td>12.2875</td>\n",
       "      <td>NaN</td>\n",
       "      <td>S</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   PassengerId                                          Name   Age  SibSp  \\\n",
       "0          892                              Kelly, Mr. James  34.5      0   \n",
       "1          893              Wilkes, Mrs. James (Ellen Needs)  47.0      1   \n",
       "2          894                     Myles, Mr. Thomas Francis  62.0      0   \n",
       "3          895                              Wirz, Mr. Albert  27.0      0   \n",
       "4          896  Hirvonen, Mrs. Alexander (Helga E Lindqvist)  22.0      1   \n",
       "\n",
       "   Parch   Ticket     Fare Cabin Embarked  Pclass_2  Pclass_3  Sex_male  \\\n",
       "0      0   330911   7.8292   NaN        Q         0         0         1   \n",
       "1      0   363272   7.0000   NaN        S         0         0         0   \n",
       "2      0   240276   9.6875   NaN        Q         0         0         1   \n",
       "3      0   315154   8.6625   NaN        S         0         0         1   \n",
       "4      1  3101298  12.2875   NaN        S         0         0         0   \n",
       "\n",
       "   FamilyNum  \n",
       "0          0  \n",
       "1          1  \n",
       "2          0  \n",
       "3          0  \n",
       "4          2  "
      ]
     },
     "execution_count": 54,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "titanic_test['FamilyNum'] = titanic_test['SibSp'] + titanic_test['Parch']\n",
    "titanic_test.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "接下来构建我们要输入给模型进行预测的变量，需要和模型训练时的输入一致。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_test = titanic_test[['Age', 'FamilyNum', 'Pclass_2', 'Pclass_3', 'Sex_male']]\n",
    "X_test = sm.add_constant(X_test)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "现在就可以调用逻辑回归模型的`predict`方法，获得预测的幸存概率。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0      0.478514\n",
       "1      0.879434\n",
       "2      0.236473\n",
       "3      0.552361\n",
       "4      0.940242\n",
       "         ...   \n",
       "413    0.520230\n",
       "414    0.925647\n",
       "415    0.439306\n",
       "416    0.520230\n",
       "417    0.411858\n",
       "Length: 418, dtype: float64"
      ]
     },
     "execution_count": 56,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "predicted_value = model.predict(X_test)\n",
    "predicted_value"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "我们获得了逻辑回归模型预测的`titanic_test.csv`里，泰坦尼克号乘客的幸存概率。我们可以把概率大于等于0.5的预测为幸存，小于0.5的预测为遇难，输出一下这个最终的预测结果。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0      False\n",
       "1       True\n",
       "2      False\n",
       "3       True\n",
       "4       True\n",
       "       ...  \n",
       "413     True\n",
       "414     True\n",
       "415    False\n",
       "416     True\n",
       "417    False\n",
       "Length: 418, dtype: bool"
      ]
     },
     "execution_count": 57,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "predicted_value > 0.5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
