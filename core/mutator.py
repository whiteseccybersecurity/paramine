from urllib.parse import quote

def mutate_payload(payload):

    return list(set([

        payload,

        quote(payload),

        payload.upper(),

        payload.lower(),

        payload.replace(
            "<",
            "%3C"
        ).replace(
            ">",
            "%3E"
        ),

        payload.replace(
            "script",
            "scr<script>ipt"
        )

    ]))
