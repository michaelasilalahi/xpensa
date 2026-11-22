import {
  View,
  Text,
  ActivityIndicator,
  Dimensions,
  FlatList,
} from 'react-native';
import { useGoogleStore } from '@/auth/google';
import {
  ProgressBar,
  AnalysisDisabled,
  DataMiningResult,
} from '@/features/archive-calender';
import { useInsightStatus } from '../hooks/insightStatus.hooks';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

interface InsightProps {
  month: number;
  year: number;
}

export const Insight = ({ month, year }: InsightProps) => {
  const user = useGoogleStore((state) => state.user);
  const userId = user?.id || '';

  const { loading, status, results, progressData } = useInsightStatus(
    userId,
    month,
    year,
  );

  // tampilan loading untuk saat cek status database
  if (status === 'checking' || loading) {
    return (
      <View className='flex-1 justify-center items-center bg-white'>
        <ActivityIndicator size='large' color='black' />
        <Text className='mt-4 font-montserrat-medium text-gray-500'>
          Memeriksa Data Siklus Kustom...
        </Text>
      </View>
    );
  }

  // tampilan disabled jika status disabled
  if (status === 'disabled' && progressData) {
    return (
      <View className='flex-1 bg-white px-4'>
        <AnalysisDisabled message={progressData.message} />
      </View>
    );
  }

  // tampilan progress bar
  if (status === 'insufficient' && progressData) {
    return (
      <View className='flex-1 bg-white pt-[30px] px-4'>
        <View className='mb-4'>
          <ProgressBar progressBarData={progressData} isLoading={loading} />
        </View>
      </View>
    );
  }

  if (status === 'completed' && results.length > 0) {
    return (
      <View className='flex-1 bg-white'>
        <View style={{ flex: 1 }}>
          <FlatList
            data={results}
            keyExtractor={(_, index) => index.toString()}
            horizontal
            pagingEnabled
            showsHorizontalScrollIndicator={false}
            renderItem={({ item }) => (
              <View style={{ width: SCREEN_WIDTH, flex: 1 }}>
                <DataMiningResult {...item} />
              </View>
            )}
          />
        </View>
      </View>
    );
  }

  return (
    <View className='flex-1 py-[50px] w-[90%] mx-auto'>
      <View className='gap-y-[15px] py-[15px] px-[15px] items-center rounded-[15px] border-[#AAAAAA] border-[0.5px]'>
        <View className='flex gap-y-[30px]'>
          <Text className='font-montserrat-semibold text-center'>
            Belum Ada Pola Terdeteksi.
          </Text>
          <Text className='font-montserrat-medium text-gray-500 text-center leading-7'>
            Terus catat pengeluaran Keinginan Anda dengan disiplin. Semakin
            banyak data yang terkumpul, semakin akurat sistem kami dalam
            membantu Anda mencegah keborosan.
          </Text>
        </View>
      </View>
    </View>
  );
};
