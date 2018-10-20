from MetaDataApi.datapoints.models import CategoryTypes, DatapointV2, RawData, MetaData


class ProcessRawData:

    def select_mutate_variant(self, category):
        functionlist = dict()
        for e in CategoryTypes:
            functionlist[e.name] = getattr(ProcessRawData, e.name)

        # Get the function from functionlist dictionary
        func = functionlist.get(CategoryTypes(category).name)
        # Execute the function
        return func

    def default_response(self, info, source, category, label, starttime, stoptime,
                         value, std, text):

        metadata = MetaData.object.get(
            source=source,
            category=category,
            label=label,
            raw=false
        )

        return [
            DatapointV2(
                starttime=starttime,
                stoptime=stoptime,
                value=value,
                std=std,
                metadata=metadata,
                owner=info.context.user
            ),
            RawData(
                starttime=starttime,
                stoptime=stoptime,
                image=None,
                audio=None,
                value=value,
                std=std,
                text=text,
                owner=info.context.user
            )
        ]

    def speech(self, info, source, category, label, starttime, stoptime=None,
               value=None, std=None, text=None, files=None):

        uploaded_image = uploaded_audio = None

        if files != None:
            # make sure which one is the image, audio
            # currently we are assuming the first one is image, the second audio
            # uploaded_image = info.context.FILES.get(files[0])
            uploaded_audio = info.context.FILES["0"]

        valid_voice_list = ["Speech", "Dialog", "Laughter"]

        profile = Profile.objects.get(user=info.context.user)

        if uploaded_audio is None:
            raise GraphQLError("no audiofile recieved")
        else:
            text = ""

            # try:
            #    raise ValueError('not implemented fully yet')
            #    sound_clasifier = SoundClassifier()
            #    predictions = sound_clasifier.classify_sound(uploaded_audio)

            #    best_keywords = list(map(lambda x: x[0], predictions))

            #    if not set(best_keywords) & set(valid_voice_list):
            #        text_from_audio = "!V! "
            #        #text_from_audio = "Not voice, more likely: " + " or ".join(best_keywords)
            # except Exception as e:
            #    print(e)

            try:
                text += transcribe_file(uploaded_audio,
                                        profile.language) if (uploaded_audio != None) else None
            except ValueError as e:
                print(e)

        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)

    def test(self, info, source, category, label, starttime, stoptime=None,
             value=None, std=None, text=None, files=None):

        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)

    def diet(self, info, source, category, label, starttime, stoptime=None,
             value=None, std=None, text=None, files=None):
        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)

    def sleep(self, info, source, category, label, starttime, stoptime=None,
              value=None, std=None, text=None, files=None):
        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)

    def phys_act(self, info, source, category, label, starttime, stoptime=None,
                 value=None, std=None, text=None, files=None):
        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)

    def ment_act(self, info, source, category, label, starttime, stoptime=None,
                 value=None, std=None, text=None, files=None):
        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)

    def body_meas(self, info, source, category, label, starttime, stoptime=None,
                  value=None, std=None, text=None, files=None):
        return self.default_response(info, source, category, label, starttime, stoptime, value, std, text)
