import '../styles/globals.css'

import type { AppProps } from 'next/app'
import { DataContextProvider } from 'contexts/data'
import { Layout } from 'components/common/layout'

function MyApp({ Component, pageProps }: AppProps) {
  return <DataContextProvider>
    <Layout>
      <Component {...pageProps} />
    </Layout>
  </DataContextProvider>
}

export default MyApp
