import re
stmt_comment = "if(tvibptr->stype =='1'){  /* blah \n bleh */;\nyes=findverb;}\n/* foo  */\n"
# stmt_comment = "if(tvibptr->stype =='1'){ /* blah */yes=findverb;}/*  */"
# stmt_comment = "if(tvibptr->stype =='1') yes=findverb;"
stmt_var_decl_initialized = "int yes=0,success=1;char t='ty'"
stmt_assignment = "choice = (3 + 4 * 8 % 3) / 7;\n a=b; // rest of line a comment "
stmt_func_decl_simple = "int gcd(unsigned char u, int v)\n{ if(v==2) return u - v * w;}"
stmt_func_decl_complex = "int gcd(int u, int v){ if(v==k) return u * v/(w+r); else return gcd(v, v + (u-v)/(v-u));}"
stmt_func_decl_complex1 = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean)"
stmt_func_decl_complex2 = "int choice(int type, unsigned char *word){if(stype!='kartari') {choice = (3 + 4 * 8) / 7; blah = gcd->yt - rt->uy} else choice = rt->uy;}"
stmt_func_def_complex1 = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean){" \
                         "int yes=0,success=1;" \
                         "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4')" \
                         "		{/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                         "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}return success;}"
stmt_func_def_complex2 = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean){while(1){" \
                         "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4'){" \
                         "/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                         "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )" \
                         "{switch(tvibptr->spos){" \
                         "case 0:if(tvibptr->semlinga==0)strcat(tvibptr->arthaword,'×Ú ');if(tvibptr->semlinga==1)strcat(tvibptr->arthaword,'×£ ');if(tvibptr->semlinga==2)strcat(tvibptr->arthaword,'ÂèÂ ');break;" \
                         "case 1:strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');break;" \
                         "case 2:strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break;" \
                         "case 3:strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                         "case 4:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                         "case 5:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;}}" \
                         "if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')success= 0;}if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)){" \
                         "       /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */" \
                         "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}" \
                         "/* If not in above case following steps lead to menu display for   selection based on type of vibhakti */ " \
                         "if(tvibptr->stype =='1') { switch(tvibptr->spos) {" \
                         "case 0:if(strcmpi(voice,'kartari') ==0)strcpy(tvibptr->arthaword,tvibptr->sword);if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ');}break;" \
                         "case 1:if(strcmpi(voice,'kartari') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');}if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->sword);}break; " \
                         "case 2:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break; " \
                         "case 3:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                         "case 4:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                         "case 6:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ ');break; " \
                         "case 5:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;} } " \
                         "if (tvibptr->next != NULL)tvibptr=tvibptr->next; else break;}return success;}"
stmt_assignment_func = 'choice = strcmpi(voice,"karmani")==0'
stmt_if_assign = 'if(a==0 && a == b || strcmp(temp->Type,"Noun")==0) choice = rt->uy;'
stmt_if_assign2 = 'if(a==0 && a == b || strcmp(temp->Type,"Noun")==0) choice = rt->uy;' \
                  'if(strcmp(temp->Type,"Noun")==0 && strcmp(temp->specf,"Subject")==0 && temp->subinsen==0){Assignlingavib(drecord);break;}' \
                  'if(temp->next != NULL)temp=temp->next;else break;'
stmt_if_assign3 = 'if(a==b){Assignlingavib(drecord);break};\nelse temp=temp->next;'
stmt_strcmp_cpy_cat = 'if(strcmpi(voice,"karmani") ==0) \
      					{ \
      						strcpy(tvibptr->arthaword,tvibptr->bword); \
      						strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ");if(strcmpi(voice,"karmani") ==0) strcpy(tvibptr->arthaword,tvibptr->bword);}'
stmt_switch_case = 'switch(spos) { case 0: choice = 3; break; case "1": i = 1; break; default: j = "ikh"}'
stmt_switch_case1 = 'switch(spos) { case 0: case "1": i = 1; break; case 3: kk == mm; gg = 99; default: j = "ikh"}'  #
stmt_switch_case2 = 'switch(tvibptr->spos) {case 0:if(strcmpi(voice,"kartari") ==0) strcpy(tvibptr->arthaword,tvibptr->sword);' \
                    'if(strcmpi(voice,"karmani") ==0) strcpy(tvibptr->arthaword,tvibptr->sword);' \
                    'case "1": if(strcmpi(voice,"karmani") ==0)strcpy(tvibptr->arthaword,tvibptr->sword); break; case 3: j = "ikh"}'
stmt_switch_case22 = 'switch(tvibptr->spos) {case 0:i = 1; break; case "1": choice = 3; break; case 3: j = "ikh"}'
stmt_switch_case3 = 'switch(tvibptr->spos) {' \
                    'case 0:if(strcmpi(voice,"kartari") ==0)strcpy(tvibptr->arthaword,tvibptr->sword);' \
                    'if(strcmpi(voice,"karmani") ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ");}break;' \
                    'case 1:if(strcmpi(voice,"kartari") ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ");}' \
                    'if(strcmpi(voice,"karmani") ==0){strcpy(tvibptr->arthaword,tvibptr->sword);}break;' \
                    ' case 2:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ");break;' \
                    ' case 3:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ");break;' \
                    ' case 4:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ");break; ' \
                    'case 6:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"×ÌèÊÆèÅÛ ");break; ' \
                    'case 5:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ");break;' \
                    '}'
stmt_while = 'while(1){if(strcmp(temp->Type,"Noun")==0 && strcmp(temp->specf,"Subject")==0 && temp->subinsen==0){Assignlingavib(drecord);break;}if(temp->next != NULL)temp=temp->next;else break;}'
stmt_if_while_complex1 = "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4')" \
                      "		{/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                      "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}"
stmt_while_complex2 = "while(1)  { " \
                      "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4') " \
                      "{ /* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */  " \
                      "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);   " \
                      "if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )  {" \
                      "   switch(tvibptr->spos)   {" \
                      "  case 0:   if(tvibptr->semlinga==0)    strcat(tvibptr->arthaword,'×Ú ');" \
                      "   if(tvibptr->semlinga==1)    strcat(tvibptr->arthaword,'×£ ');" \
                      "   if(tvibptr->semlinga==2)    strcat(tvibptr->arthaword,'ÂèÂ ');   break;  " \
                      "case 1:   strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');   break;  " \
                      "case 2:   strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');   break;  " \
                      "case 3:   strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');   break;  " \
                      "case 4:   strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');   break;  " \
                      "case 5:   strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');   break;   }" \
                      "  }  if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')   success= 0;  } " \
                      "if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)) {" \
                      "    /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */  " \
                      "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean); }}"
stmt_while_complex3 = "while(1){" \
                      "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4'){" \
                      "/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                      "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )" \
                      "{switch(tvibptr->spos){" \
                      "case 0:if(tvibptr->semlinga==0)strcat(tvibptr->arthaword,'×Ú ');if(tvibptr->semlinga==1)strcat(tvibptr->arthaword,'×£ ');if(tvibptr->semlinga==2)strcat(tvibptr->arthaword,'ÂèÂ ');break;" \
                      "case 1:strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');break;" \
                      "case 2:strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break;" \
                      "case 3:strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                      "case 4:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                      "case 5:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;}}" \
                      "if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')success= 0;}if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)){" \
                      "       /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */" \
                      "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}" \
                      "/* If not in above case following steps lead to menu display for   selection based on type of vibhakti */ " \
                      "if(tvibptr->stype =='1') { switch(tvibptr->spos) {" \
                      "case 0:if(strcmpi(voice,'kartari') ==0)strcpy(tvibptr->arthaword,tvibptr->sword);if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ');}break;" \
                      "case 1:if(strcmpi(voice,'kartari') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');}if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->sword);}break; " \
                      "case 2:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break; " \
                      "case 3:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                      "case 4:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                      "case 6:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ ');break; " \
                      "case 5:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;} } " \
                      "if (tvibptr->next != NULL)tvibptr=tvibptr->next; else break;}"
stmt_include = "#include <stdio.h>\n"
stmt_include2 = '#include "sengen1.h"\n'
stmt_include3 = '#include "data.h"\n'
stmt_define = "#define KARTHARI    0; #define KARMANI     1; #define FULLSTOP  'ê'; #define eof       255"
stmt_typedef = "typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int purusha[20]; unsigned char *subanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];         /* End Removed Base */; int wordNum[20]; int numofNouns; } SUBANTA_DATA;"
stmt_typedef_many = "typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int purusha[20]; unsigned char *subanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];         /* End Removed Base */; int wordNum[20]; int numofNouns; } SUBANTA_DATA;  typedef struct { int dhatuVidha[10]; int prayoga[10]; int lakara[10]; int purusha[10]; int vacana[10]; int gana[10]; int padi[10]; int karma[10]; int it[10]; unsigned char *tiganta[10]; unsigned char *dhatu[10]; unsigned char *nijdhatu[10]; unsigned char *sandhatu[10]; unsigned char *artha[10]; unsigned char *err[10];    /* End Removed Root */; int wordNum[10]; int numofVerbs; } TIGANTA_DATA;  typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int prayoga[20]; int krdType[20]; int dhatuVidha[20]; int purusha[20]; int gana[20]; int padi[20]; int karma[20]; int it[20]; unsigned char *krdanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];            /* end removed base of krdanta */; unsigned char *dhatu[20]; unsigned char *nijdhatu[20]; unsigned char *sandhatu[20]; unsigned char *artha[20]; int wordNum[20]; int numofKrdantas; } KRDANTA_DATA;  typedef struct { unsigned char *avyaya[30]; int wordNum[30]; int numofAvyayas; } AVYAYA_DATA;  typedef struct { int dhatuVidha[20]; int gana[20]; int padi[20]; int karma[20]; int it[20]; int krdavType[20]; unsigned char *krdavyaya[20]; unsigned char *dhatu[20]; unsigned char *nijdhatu[20]; unsigned char *sandhatu[20]; unsigned char *artha[20]; int wordNum[20]; int numofKrdavyayas; } KRDAV_DATA;  typedef struct { unsigned char *word[20]; int vibhakti[20]; int vacana[20]; int purusha[20]; int linga[20]; int wordPos[20]; int numofWords; } VIBHAKTI;  typedef struct { unsigned char *verb; unsigned char *dhatu; int purusha; int vacana; int prayoga; int karma; int wordPos; } VERB;  typedef struct { unsigned char *krdanta; int vibhakti; int vacana; int linga; int prayoga; int karma; int krdType; } PARTICIPLE;  typedef struct { unsigned char *sentence; unsigned char *idens[100]; int numofIdens; } RECORD;  typedef struct { unsigned char *iden[30]; int numofIdens; } WORD;  typedef struct { unsigned char *word[15]; int numofWords; } TYPE;"
stmt_var_decl_array = "unsigned char list[]={'ÈÞÏèÔÚÁèØ', '¤ÈÏÚÁèØ', 'ÄÛÆ', 'ÏÚÂèÏÛ', '¤ØåÏÚÂèÏ', '×ÈèÂÚØ', 'È³èÖ', 'ÌÚ×', '×¢ÔÂè×Ï'};"
stmt_func_def_vibmenu_full = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean) { int yes=0,success=1;  while(1) { if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4') { /* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */ yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);  if(tvibptr->stype=='2' && tvibptr->matnoun !=1 ) { switch(tvibptr->spos) { case 0: if(tvibptr->semlinga==0) strcat(tvibptr->arthaword,'×Ú '); if(tvibptr->semlinga==1) strcat(tvibptr->arthaword,'×£ '); if(tvibptr->semlinga==2) strcat(tvibptr->arthaword,'ÂèÂ '); break; case 1: strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ '); break; case 2: strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ '); break; case 3: strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ '); break; case 4: strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ '); break; case 5: strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ '); break; } } if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5') success= 0;  } if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)) {        /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */ yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean); }   /* If not in above case following steps lead to menu display for    selection based on type of vibhakti */  if(tvibptr->stype =='1')  {  switch(tvibptr->spos)  { case 0: if(strcmpi(voice,'kartari') ==0) strcpy(tvibptr->arthaword,tvibptr->sword); if(strcmpi(voice,'karmani') ==0) { strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ '); } break;  case 1: if(strcmpi(voice,'kartari') ==0) { strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ '); } if(strcmpi(voice,'karmani') ==0) { strcpy(tvibptr->arthaword,tvibptr->sword); } break;  case 2: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ '); break;  case 3: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ '); break;  case 4: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ '); break;  case 6: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ '); break;  case 5: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ '); break; }  }  if (tvibptr->next != NULL) tvibptr=tvibptr->next;  else  break; } return success; }"

samples = [stmt_comment, stmt_var_decl_initialized, stmt_var_decl_array, stmt_assignment, stmt_func_decl_simple, stmt_func_decl_complex, stmt_func_decl_complex1, stmt_func_decl_complex2, stmt_func_def_complex1, stmt_func_def_complex2, stmt_assignment_func, stmt_if_assign, stmt_if_assign2, stmt_if_assign3, stmt_strcmp_cpy_cat, stmt_switch_case, stmt_switch_case1, stmt_switch_case2, stmt_switch_case22, stmt_switch_case3, stmt_while, stmt_if_while_complex1, stmt_while_complex2, stmt_while_complex3, stmt_define, stmt_include, stmt_include2, stmt_include3, stmt_typedef_many, stmt_func_def_vibmenu_full]

pattern_crlf, pattern_spaces_2_or_more, pattern_tabs, pattern_c_strcmp, pattern_c_strcpy, pattern_c_strcat, \
    pattern_include, pattern_define,  pattern_nl, pattern_star_slash, pattern_star_slash_semicolon = \
        re.compile(r"\r\n"), re.compile(" +"), re.compile("\t+"), re.compile("strcmpi?\((.+?),(.+?)\)\s*==\s*0"), \
        re.compile("strcpy\((.+?)\s*,\s*(.+?)\)"), re.compile("strcat\(\s*(.+?)\s*,\s*(.+?)\s*\)"),\
        re.compile(r"#include(.+)"), re.compile(r"#define(.+)"), re.compile(r"\n$"), re.compile(r"\*\/"),  re.compile(r"\*\/;")
