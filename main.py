from benchmark import JssBenchmark

if __name__ == '__main__':
    benchmark = JssBenchmark(folder_path='./data', output_path='output')
    benchmark.run()
