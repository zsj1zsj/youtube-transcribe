import ffmpeg
import os


# downgrade sample rate to 16000
def downgrade_sample_rate(input_file, output_file):
    input_file = input_file
    output_file = output_file
    print("file path: " + input_file)
    (
        ffmpeg
        .input(input_file)
        .output(
            output_file,
            ar=16000,  # 设置采样率为 16000Hz
            ac=1,      # 设置声道数为 1（单声道）
            map='0:a'  # 映射第一个音频流
        )
        .overwrite_output()  # 如果输出文件已存在，则覆盖
        .run()
    )
    
# 切割视频，暂时可以根据大小进行切割，N = 文件大小/20M，分割成N份
# 还需要知道音频的时长， 视频之间应该有一定的重叠（防止有信息丢失）
def split_audio(input_file, output_prefix, num_parts, overlap_seconds):
    # 获取音频文件的总时长（以秒为单位）
    probe = ffmpeg.probe(input_file)
    duration = float(probe['streams'][0]['duration'])
    
    # 计算每个部分的时长（不包括重叠部分）
    part_duration = (duration - overlap_seconds) / num_parts
    
    for i in range(num_parts):
        start_time = i * part_duration
        end_time = (i + 1) * part_duration + overlap_seconds
        
        # 确保最后一部分不超过音频总时长
        if i == num_parts - 1:
            end_time = duration
        
        output_file = f"{output_prefix}_{i+1}.mp3"
        
        # 使用ffmpeg-python进行切割
        stream = ffmpeg.input(input_file, ss=start_time, t=end_time-start_time)
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
        
        print(f"Part {i+1} created: {output_file}")
    
if __name__ == "__main__":
    downgrade_sample_rate('北约积极介入亚太事务剑指中共⧸新闻8分钟⧸王剑每日观察.m4a',
                          '北约积极介入亚太事务剑指中共⧸新闻8分钟⧸王剑每日观察.m4a')