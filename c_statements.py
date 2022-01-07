import re
stmt_comment = "if(tvibptr->stype =='1'){  /* blah \n bleh */;\nyes=findverb;}\n/* foo  */\n"
# stmt_comment = "if(tvibptr->stype =='1'){ /* blah */yes=findverb;}/*  */"
# stmt_comment = "if(tvibptr->stype =='1') yes=findverb;"
stmt_var_decl_initialized = "int yes=0,success=1;char t='ty'"
stmt_assignment = "choice = (3 + 4 * 8 % 3) / 7;\n a=b; type[i]=words[3][0]; type[a][b]=words[c][d][e]; // rest of line a comment "
stmt_func_decl_default = "int gcd(unsigned char u, int v)\n{ if(v==2) return u - v * w;}fdisp(FILE *sfp,VIBAK *dvibptr,DISP_ARTH *start,unsigned char voice[]);"
stmt_func_decl_complex = "int gcd(int u, int v){ if(v==k) return u * v/(w+r); else return gcd(v, v + (u-v)/(v-u));}; empty_return(int y) return; unsigned char * asrPhoneticJoin( char *);"
stmt_func_decl_complex1 = "int choice(char type,unsigned char *word,unsigned char voice[], unsigned char vice[ik-k],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean)"
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
stmt_if_assign4 = 'if(strcmp(word,list1[i])==0) {if(linga==0) strcpy(message,"×ÌÔáÂÚ");  ' \
                  'if(linga==1) strcpy(message,"×ÌÔáÂ£");if(linga==2) strcpy(message,"×ÌÔáÂ¢");' \
                 'strcpy(vword,tvibptr->bword);  strcat(vword,message);  strcpy(tvibptr->arthaword,vword);return 1; } '
stmt_strcmp_cpy_cat = 'if(strcmpi(voice,"karmani") ==0) \
      					{ \
      						strcpy(tvibptr->arthaword,tvibptr->bword); \
      						strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ");if(strcmpi(voice,"karmani") ==0) strcpy(tvibptr->arthaword,tvibptr->bword);}'
stmt_switch_case = 'switch(spos) { case 0: choice = 3; bb=cc; break; case "1": i = 1; break; default: j = "ikh"}'
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
stmt_include2 = '#include "sengen1.h"\n #include "data.h"\n'
stmt_define = "#define KARTHARI    0 #define KARMANI     1 #define HALANT (unsigned char)'è' #define FULLSTOP  'ê' #define eof       255 "
stmt_typedef = "typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int purusha[20]; unsigned char *subanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];         /* End Removed Base */; int wordNum[20]; int numofNouns; } SUBANTA_DATA;"
stmt_typedef_many = "typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int purusha[20]; unsigned char *subanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];         /* End Removed Base */; int wordNum[20]; int numofNouns; } SUBANTA_DATA;  typedef struct { int dhatuVidha[10]; int prayoga[10]; int lakara[10]; int purusha[10]; int vacana[10]; int gana[10]; int padi[10]; int karma[10]; int it[10]; unsigned char *tiganta[10]; unsigned char *dhatu[10]; unsigned char *nijdhatu[10]; unsigned char *sandhatu[10]; unsigned char *artha[10]; unsigned char *err[10];    /* End Removed Root */; int wordNum[10]; int numofVerbs; } TIGANTA_DATA;  typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int prayoga[20]; int krdType[20]; int dhatuVidha[20]; int purusha[20]; int gana[20]; int padi[20]; int karma[20]; int it[20]; unsigned char *krdanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];            /* end removed base of krdanta */; unsigned char *dhatu[20]; unsigned char *nijdhatu[20]; unsigned char *sandhatu[20]; unsigned char *artha[20]; int wordNum[20]; int numofKrdantas; } KRDANTA_DATA;  typedef struct { unsigned char *avyaya[30]; int wordNum[30]; int numofAvyayas; } AVYAYA_DATA;  typedef struct { int dhatuVidha[20]; int gana[20]; int padi[20]; int karma[20]; int it[20]; int krdavType[20]; unsigned char *krdavyaya[20]; unsigned char *dhatu[20]; unsigned char *nijdhatu[20]; unsigned char *sandhatu[20]; unsigned char *artha[20]; int wordNum[20]; int numofKrdavyayas; } KRDAV_DATA;  typedef struct { unsigned char *word[20]; int vibhakti[20]; int vacana[20]; int purusha[20]; int linga[20]; int wordPos[20]; int numofWords; } VIBHAKTI;  typedef struct { unsigned char *verb; unsigned char *dhatu; int purusha; int vacana; int prayoga; int karma; int wordPos; } VERB;  typedef struct { unsigned char *krdanta; int vibhakti; int vacana; int linga; int prayoga; int karma; int krdType; } PARTICIPLE;  typedef struct { unsigned char *sentence; unsigned char *idens[100]; int numofIdens; } RECORD;  typedef struct { unsigned char *iden[30]; int numofIdens; } WORD;  typedef struct { unsigned char *word[15]; int numofWords; } TYPE;"
stmt_var_decl_array = "unsigned char list[]={'ÈÞÏèÔÚÁèØ', '¤ÈÏÚÁèØ', 'ÄÛÆ', 'ÏÚÂèÏÛ', '¤ØåÏÚÂèÏ', '×ÈèÂÚØ', 'È³èÖ', 'ÌÚ×', '×¢ÔÂè×Ï'}; unsigned char list[jk-ui]; unsigned char list[i+9]={'ÈÞÏèÔÚÁèØ', '¤ÈÏÚÁèØ', 'ÄÛÆ', 'ÏÚÂèÏÛ', '¤ØåÏÚÂèÏ', '×ÈèÂÚØ', 'È³èÖ', 'ÌÚ×', '×¢ÔÂè×Ï'};"
stmt_func_def_vibmenu_c_complete = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean) { int yes=0,success=1;  while(1) { if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4') { /* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */ yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);  if(tvibptr->stype=='2' && tvibptr->matnoun !=1 ) { switch(tvibptr->spos) { case 0: if(tvibptr->semlinga==0) strcat(tvibptr->arthaword,'×Ú '); if(tvibptr->semlinga==1) strcat(tvibptr->arthaword,'×£ '); if(tvibptr->semlinga==2) strcat(tvibptr->arthaword,'ÂèÂ '); break; case 1: strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ '); break; case 2: strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ '); break; case 3: strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ '); break; case 4: strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ '); break; case 5: strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ '); break; } } if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5') success= 0;  } if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)) {        /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */ yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean); }   /* If not in above case following steps lead to menu display for    selection based on type of vibhakti */  if(tvibptr->stype =='1')  {  switch(tvibptr->spos)  { case 0: if(strcmpi(voice,'kartari') ==0) strcpy(tvibptr->arthaword,tvibptr->sword); if(strcmpi(voice,'karmani') ==0) { strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ '); } break;  case 1: if(strcmpi(voice,'kartari') ==0) { strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ '); } if(strcmpi(voice,'karmani') ==0) { strcpy(tvibptr->arthaword,tvibptr->sword); } break;  case 2: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ '); break;  case 3: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ '); break;  case 4: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ '); break;  case 6: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ '); break;  case 5: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ '); break; }  }  if (tvibptr->next != NULL) tvibptr=tvibptr->next;  else  break; } return success; }"
stmt_for = 'for(i=0;i<vno;i-=3) free(words[i]); for(i=j+1,k=0;i<strlen(word);i+=2,k++)  {s=u;};for(i=0;input[i]!= "\0";i++);'
stmt_increment_decrement = 'i++;j--;k+=2;h-=3;recptr->no_base++;recptr->no_codes--;'
stmt_func_def_complex3 = 'int findverb(unsigned char voice[],unsigned char *Word,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean)' \
                 '{int found=0,i,j,pos;int vnum=0,vno=0,linga=4;unsigned char line1[300],*words[17],message[60],word[20],vword[80],type,' \
                 'lword[30],ltype="Z",temp[4];unsigned char *list[]={"ÈÞÏèÔÚÁèØ", "¤ÈÏÚÁèØ", "ÄÛÆ", "ÏÚÂèÏÛ", "¤ØåÏÚÂèÏ", "×ÈèÂÚØ", "È³èÖ", "ÌÚ×", "×¢ÔÂè×Ï"};' \
                 'unsigned char *list1[]={"ºè¼ÚÆ","×Ý´","ÄÝ£´","¦¸è¹Ú","ÄèÔáÖ","ÈèÏÍÂèÆ","ÅÏèÌ","¤ÅÏèÌ","×¢×è³ÚÏ","ËÚÔÆÚ","ÔÛÔá³","ÊåÅ","ÊÝÄèÅÛ","ÅÜ","ÈèÏºè¼Ú",};' \
                 'fseek(afp,fl,0);}if(tvibptr->stype =="2") type="0";' \
                 ' while(found==0  ||(!feof(afp))){fgets(line1,299,afp);if(line1[0]==" - "){found=1;break;}vno=0;vno=split(line1,words);' \
                 'if(strcmp(words[0],"ÔÚ³èÍÌè")==0) {for(i=0;i<vno;i++){free(words[i]);continue;}}' \
                 'vno=0; vno=split(line1,words); ' \
                 'if(strcmp(words[0],"ÔÚ³èÍÌè")==0) /* Check for input sentence */ ' \
                 '{  for(i=0;i<vno;i++) free(words[i]);  continue; }' \
                 ' vno=split(line1,words); type=words[3][0]; strcpy(word,words[4]); ' \
                 'if(type=="1") {  strncpy(temp,words[6]+2,1);  temp[1]="\0";  linga=atoi(temp);  pos=atoi(words[7]); }' \
                 ' if(type=="5" || type=="4") {  if(type=="5") strcpy(lword,VerbMean);  else  { strcpy(lword,words[9]);  }' \
                 '  strncpy(temp,words[11]+1,1);  temp[1]="\0";  ltype=temp[0]; }' \
                 ' if(type=="2") {  strcpy(lword,words[13]); }' \
                 ' if(type=="1"&& (pos >= 1 && pos <=3)) {' \
                 '  for(i=0;i<15;i++)  ' \
                 '{ if(strcmp(word,list1[i])==0) {' \
                 '  if(linga==0) strcpy(message,"×ÌÔáÂÚ");  ' \
                 'if(linga==1) strcpy(message,"×ÌÔáÂ£");' \
                 'if(linga==2) strcpy(message,"×ÌÔáÂ¢");' \
                 '  strcpy(vword,tvibptr->bword);  strcat(vword,message);  strcpy(tvibptr->arthaword,vword);' \
                 '  return 1; }  } } ' \
                 'if(type=="5") {  found=dispmea(voice,vnum,list,tvibptr,ltype,lword);  for(i=0;i<vno;i++) free(words[i]);  return found; } ' \
                 'if(type=="2" && tvibptr->stype=="2" && strcmp(Word,words[1])==0) {  found=dispmea(voice,vnum,list,tvibptr,ltype,lword);  ' \
                 'for(i=0;i<vno;i++) free(words[i]);  return found; } else if(type=="4" && tvibptr->stype=="4" && strcmp(Word,words[1])==0) ' \
                 '{  found=dispmea(voice,vnum,list,tvibptr,ltype,lword);  for(i=0;i<vno;i++) free(words[i]);  return found; } ' \
                 'for(i=0;i<vno;i++)  free(words[i]);};'
stmt_assignment_and_condition = 'a = b; message = "×ÌÔáÂ£"; if(c=fgetc(cfp)!=eof) x = y'
stmt_multilevel_indices_pointers = 'substr=strstr(word[karptr->sub_no],krdrecord->code[m][n])'
stmt_includes_defines_others = '#include <stdio.h> #include <string.h> #include <stdlib.h> #include <conio.h> #include <alloc.h> #include "data.h" #include "declr.h" #define eof 255 #define rt 86 int CheckComptability(DETAIL *srecord,DETAIL *krecord,DETAIL *vrecord,DETAIL *krdfirst,DETAIL *krdavy,unsigned char *sent,SHASTI *fshtptr,FILE *rfp,FILE *afp,FILE *sfp,int y) { int a=0,i=0,j=0,m=0,n=0,no_vsub=0,no_ksub=0,num_sub,Naflag=0; int flag=1,krdflag=0,krdavyf=0,verflag=0,karflag=0,shaflag=0; int krdmismatch=0,mismatch=0,krdpos,avypos,Saflag=0,Sapos; int krdoth=0,no_krdoth,krdsuc=1,subver=0; long afppos,pos; unsigned char c,line[500],*word[15],temp[150],*substr,temp1[30],temp2[30]; char code1[5],code2[5]; FILE *cfp; DETAIL *firstptr=NULL,*subptr=NULL,*fstptr=NULL,*subunmatch; DETAIL *karptr=NULL,*un_match=NULL,*karmatch=NULL; DETAIL *verptr=NULL,*krdrecord=NULL,*krdunmatch=NULL,*krdmatch=NULL,*avyrecord=NULL; SHASTI *shrvib=NULL,*tshrvib=NULL;int a=0,i=0,j=0,m=0,n=0,no_vsub=0,no_ksub=0,num_sub,Naflag=0; int flag=1,krdflag=0,krdavyf=0,verflag=0,karflag=0,shaflag=0; int krdmismatch=0,mismatch=0,krdpos,avypos,Saflag=0,Sapos; int krdoth=0,no_krdoth,krdsuc=1,subver=0; long afppos,pos; unsigned char c,line[500],*word[15],temp[150],*substr,temp1[30],temp2[30]; char code1[5],code2[5]; FILE *cfp; DETAIL *firstptr=NULL,*subptr=NULL,*fstptr=NULL,*subunmatch; DETAIL *karptr=NULL,*un_match=NULL,*karmatch=NULL; DETAIL *verptr=NULL,*krdrecord=NULL,*krdunmatch=NULL,*krdmatch=NULL,*avyrecord=NULL; SHASTI *shrvib=NULL,*tshrvib=NULL; cfp=fopen("comptble.aci","r"); if(cfp== NULL) exit(0); firstptr=srecord; subptr=srecord; fstptr=srecord; while(1) { if(strcmp(subptr->word,"Æ")==0) Naflag=1; else if(strcmp(subptr->word,"×Ø")==0) { Saflag=1; Sapos=subptr->pos; } if(subptr->next != NULL) subptr=subptr->next; else break; } subptr=srecord; karptr=krecord; verptr=vrecord; krdrecord=krdfirst; avyrecord=krdavy; krdpos=0;if(krdfirst != NULL) { if(strcmp(krdrecord->Type,"Krdanta")==0 || strcmpi(krdrecord->specf,"Subject")==0) { krdflag=1; krdpos=krdrecord->pos; } } if(krdavy != NULL) { if(strcmpi(krdavy->Type,"Krdavyaya")==0) krdavyf=1; } verflag=0; while(verptr != NULL) { if(strcmp(verptr->dispSpecf,"Verb")==0) verflag=1; if(verptr->next == NULL) break; verptr=verptr->next; } verptr=vrecord;while(1) { if(karptr != NULL && krdflag==0 && krdavyf==0) { if(karptr->sub_no != 7 && (karptr->pos != Sapos-1)) no_vsub++; if(karptr->next != vrecord) karptr=karptr->next; else break; } else if(karptr != NULL && verflag==1 && krdflag==1) { if(karptr->sub_no != 6) { if (karptr->pos > krdfirst->pos ) no_vsub++; else if(strcmp(krdfirst->specf,"Subject")!=0) no_vsub++; } else if(karptr->sub_no == 6) { if (karptr->pos != krdfirst->pos-1 ) no_vsub++; else if(strcmp(krdfirst->specf,"Subject")!=0) no_vsub++; } if(karptr->next != krdfirst) karptr=karptr->next; else break; } else if(karptr != NULL && verflag==1 && krdavyf==1) { if (karptr->pos > krdavy->pos) no_vsub++; if(karptr->next != krdavy) karptr=karptr->next; else break; } else break; }fprintf(rfp,"%s \n",sent); karptr=krecord; if(fshtptr==NULL) { while(1) { fprintf(rfp,"%s ", subptr->Type); if(strcmp(subptr->Type,"Noun")==0 || strcmp(subptr->Type,"Krdanta")==0 ) fprintf(rfp,"%s",subptr->specf); fprintf(rfp," : %s",subptr->word); fprintf(rfp,"\n"); if(subptr->next != NULL) subptr=subptr->next; else break; } subptr=srecord; shaflag=0; } else { sha_disp(subptr,sent,rfp); shaflag=1; }fprintf(rfp,"\n-------------------\n");  karptr=krecord;  subptr=srecord;  if(vrecord==NULL)   vrecord=krdfirst;  verptr=vrecord;}'
stmt_multilevel_pointers_indices_and_assigned_conditions = 'while(strcmpi(srecord->specf,"subject")==0 && strcmpi(srecord->Type,"Noun")==0) { if(krdflag==1) { for(m=0;m<(krdrecord->no_base);m++) ' \
                 '{ num_sub=no_ksub; karflag=0; un_match=NULL; if(karptr != NULL) { while(1) { if(strcmp(krdrecord->specf,"Subject")==0) ' \
                 '{ if(karptr->pos < krdrecord->pos && karptr != NULL ) { if(karptr->sub_no != 6) karflag++; } } ' \
                 'if(strcmpi(karptr->next->Type,"Krdanta")==0 ||strcmpi(karptr->next->Type,"Krdavyaya")==0 ) break; else karptr=karptr->next; } } krdoth=0; no_krdoth=0; ' \
                 'while(1) { if(strcmpi(krdrecord->specf,"Subject") !=0 ) { if(strcmpi(krdrecord->Type,"Krdanta") ==0 ) { no_krdoth++; krdoth++; } } ' \
                 'if(strcmpi(krdrecord->next->Type,"Krdanta") !=0 || krdrecord->next == NULL) break; else krdrecord=krdrecord->next; } krdrecord=krdfirst; ' \
                 'for(n=0;n<srecord->no_base;n++) { num_sub=no_ksub; rewind(cfp); mismatch=0; krdmismatch=0; while( (c=fgetc(cfp)) != eof) { ungetc(c,cfp); fgets(line,150,cfp);' \
                 ' if(line[0]=="\n") continue; j=split(line,word); strncpy(code1,line,2); code1[2]="\0"; karptr=krecord; krdrecord=krdfirst; ' \
                 'if(strcmp(srecord->code[n],code1)==0 ) { if(strcmp(krdrecord->Type,"Krdanta")==0 ) ' \
                 '{ if((strcmpi(srecord->voice,"kartari") == 0 && srecord->linga==krdrecord->linga && srecord->vibvach==krdrecord->vibvach) || ' \
                 'strcmpi(srecord->voice,"karmani") == 0 ) { strncpy(code2,line+3,2); code2[2]="\0"; karptr=krecord; if(karflag==0 && strcmp(code2,"00")==0) ' \
                 '{ substr=strstr(word[1],krdrecord->code[m]); if(substr) mismatch=0; else mismatch=1; } else { if(karptr != NULL) { ' \
                 'while(1) { if((karptr->pos < krdrecord->pos) && karptr!= NULL && strcmp(karptr->code[0],code2)==0) { if(karptr->sub_no !=6 ) {' \
                 ' substr=strstr(word[karptr->sub_no],krdrecord->code[m]); if(substr) { mismatch=0; karflag--; } else {' \
                 ' mismatch=1; krdunmatch=krdrecord; un_match=karptr; } } } if(strcmpi(karptr->next->Type,"Krdanta")==0) break; else karptr=karptr->next; } } } } } } ' \
                 'if(krdoth) { strncpy(code2,line+3,2); code2[2]="\0"; if(karptr != NULL) { while(1) { while(1) { if(krdrecord->sub_no !=6) {' \
                 ' if(strcmpi(krdfirst->specf,"Subject") != 0 && karptr->pos < krdrecord->pos) { } ' \
                 'if(strcmp(karptr->code[0],code1)==0 && strcmp(code2,"00")==0 && strcmp(karptr->specf,krdrecord->specf)==0 && krdrecord->matnoun==1 && ' \
                 '(karptr->pos == krdrecord->pos +1)) { substr=strstr(word[karptr->sub_no],krdrecord->code[m]); ' \
                 'if(substr && krdmismatch==0) { no_krdoth--; krdmatch=krdrecord; karmatch=karptr; } else if(!substr) { krdmismatch=1; krdunmatch=krdrecord; ' \
                 'karmatch=karptr; } break; } else if(krdrecord->matnoun != 1) { ' \
                 'if((strcmp(code1,"AA")==0 && strcmp(code2,"00")==0 ) && strcmp(krdrecord->specf,"Subject") !=0) { ' \
                 'substr=strstr(word[1],krdrecord->code[m]); if(substr && krdmismatch==0) { no_krdoth--; krdmatch=krdrecord; } else if(!substr) { krdmismatch=1; ' \
                 'krdunmatch=krdrecord; } } } } if(krdrecord->sub_no ==6) { shrvib=fshtptr ; while(strcmp(krdrecord->word,shrvib->word) !=0) shrvib=shrvib->next; ' \
                 'if(strcmp(shrvib->next->code[0],code1)==0 && strcmp(code2,"00")==0 && strcmp(karptr->specf,krdrecord->specf)==0) { ' \
                 'substr=strstr(word[1],krdrecord->code[m]); if(substr && krdmismatch==0) { no_krdoth--; krdmatch=krdrecord; karmatch=karptr; } else if(!substr) { ' \
                 'krdmismatch=1; krdunmatch=krdrecord; karmatch=karptr; } break; } } krdrecord=krdrecord->next; if(strcmp(krdrecord->Type,"Krdanta") !=0) break; ' \
                 'if(krdrecord->next == NULL) break; } krdrecord=krdfirst; if(strcmpi(karptr->next->Type,"krdanta")==0) break; else karptr=karptr->next; } } else {' \
                 ' while(strcmp(krdrecord->Type,"Verb") !=0 || krdrecord->next != NULL) { if(krdrecord->sub_no !=6) { ' \
                 'if((strcmp(code1,"AA")==0 && strcmp(code2,"00")==0 ) && strcmp(krdrecord->specf,"Subject") !=0) { substr=strstr(word[1],krdrecord->code[m]); ' \
                 'if(substr && krdmismatch==0) { no_krdoth--; krdmatch=krdrecord; } else if(!substr) { krdmismatch=1; krdunmatch=krdrecord; } } } krdrecord=krdrecord->next;' \
                 ' } } } for(i=0;i<j;i++) free(word[i]); } if(Naflag==0) { if(verflag==0) { if(!krdoth ) { if(mismatch==0 && karflag==0) { krdsuc=1; flag=1; ' \
                 'fprintf(rfp,"The Krdanta is Semantically Compatible if %s root means %s and subject is %s ",krdfirst->stem,krdfirst->base[m],srecord->base[n]); } else {' \
                 ' krdsuc=0; flag=0; fprintf(rfp,"Verb %s is not compatible with subject %s",verptr->word,srecord->word); ' \
                 'if(un_match != NULL) fprintf(rfp,"if %s is %s",un_match->dispSpecf,un_match->word); } } else if(krdoth) { if(mismatch==0 && karflag==0 && no_krdoth==0) ' \
                 '{ krdsuc=1; flag=1; if(karptr != NULL) fprintf(rfp,"%s %s %s is compatible with %s %s %s",karmatch->Type,karmatch->specf,karmatch->word,krdmatch->Type,' \
                 'krdmatch->specf,krdmatch->word); else fprintf(rfp,"%s %s %s is semantically compatible",krdmatch->Type,krdmatch->specf,krdmatch->word); ' \
                 'fprintf(rfp,"The Krdanta is Semantically Compatible if %s root means %s and subject is %s ",krdfirst->stem,krdfirst->base[m],srecord->base[n]); } ' \
                 'else if((mismatch || karflag) && ! no_krdoth) { krdsuc=0; flag=0; ' \
                 '/*fprintf(rfp,"Verb %s is not compatible with subject %s\n",verptr->word,srecord->word);*/ ' \
                 'if(mismatch) fprintf(rfp,"%s %s %s is not compatble with %s is %s",krdunmatch->Type,krdunmatch->specf,krdunmatch->word,un_match->dispSpecf,un_match->word);' \
                 ' } else if(krdmismatch==1) { krdsuc=0; flag=0; fprintf(rfp,"%s %s %s is not compatible with %s %s %s if Krdanta base is %s ",karmatch->Type,' \
                 'karmatch->specf,karmatch->word,krdunmatch->Type,krdunmatch->specf,krdunmatch->word,krdunmatch->base[0]); ' \
                 'if(un_match != NULL) fprintf(rfp,"if %s is %s ",un_match->dispSpecf,un_match->word); } } } if(verflag==1) { if(!krdoth ) { if(mismatch==0 && karflag==0) ' \
                 '{ krdsuc=1; fprintf(rfp,"The Krdanta is Semantically Compatible if %s root means %s and subject is %s ",krdfirst->stem,krdfirst->base[m],srecord->base[n])' \
                 '; } else { krdsuc=0; fprintf(rfp,"Verb %s is not compatible with subject %s ",verptr->word,srecord->word); ' \
                 'if(un_match != NULL) fprintf(rfp,"if %s is %s ",un_match->dispSpecf,un_match->word); } } else if(krdoth) { if(mismatch==0 && karflag==0 && no_krdoth==0) ' \
                 '{ krdsuc=1; if(krdmatch->matnoun==1) { if(karptr != NULL ) fprintf(rfp,"%s %s %s is compatible with %s %s %s ",karmatch->Type,' \
                 'karmatch->specf,karmatch->word,krdmatch->Type,krdmatch->specf,krdmatch->word); } ' \
                 'else fprintf(rfp,"%s %s %s is semantically compatible ",krdmatch->Type,krdmatch->specf,krdmatch->word); if(strcmp(krdfirst->Type,"Subject")==0) ' \
                 'fprintf(rfp,"The Krdanta is Semantically Compatible if %s root means %s and subject is %s ",krdfirst->stem,krdfirst->base[m],srecord->base[n]); } ' \
                 'else if((mismatch || karflag) && ! no_krdoth) { krdsuc=0; if(mismatch) fprintf(rfp,"%s %s %s is not compatble with Noun Subject if %s is %s ",' \
                 'krdunmatch->Type,krdunmatch->specf,krdunmatch->word,un_match->dispSpecf,un_match->word); } else if(krdmismatch==1) { krdsuc=0; ' \
                 'fprintf(rfp,"%s %s %s is not compatible with %s %s %s if Krdanta base is %s ",karmatch->Type,karmatch->specf,karmatch->word,krdunmatch->Type,' \
                 'krdunmatch->specf,krdunmatch->word,krdunmatch->base[0]); if(un_match != NULL) fprintf(rfp,"if %s is %s ",un_match->dispSpecf,un_match->word); } } } } ' \
                 'if(Naflag==1) { krdsuc=1; flag=1; } } } } if(krdavyf==1) { for(m=0;m<(avyrecord->no_base);m++) { num_sub=no_ksub; karflag=0; un_match=NULL; ' \
                 'while(1) { if((karptr->pos < avyrecord->pos) && karptr!= NULL) karflag++; if(strcmpi(karptr->next->Type,"Krdavyaya")==0 ) break; else karptr=karptr->next; }' \
                 ' krdrecord=krdfirst; for(n=0;n<srecord->no_base;n++) { num_sub=no_ksub; rewind(cfp); mismatch=0; krdmismatch=0; ' \
                 'while( (c=fgetc(cfp)) != eof) { ungetc(c,cfp); fgets(line,150,cfp); if(line[0]=="\n") continue; j=split(line,word); strncpy(code1,line,2); code1[2]="\0"; ' \
                 'karptr=krecord; if(strcmp(srecord->code[n],code1)==0 ) { if(strcmp(avyrecord->Type,"Krdavyaya")==0) { strncpy(code2,line+3,2); code2[2]="\0"; ' \
                 'karptr=krecord; if(karflag==0 && strcmp(code2,"00")==0) { substr=strstr(word[1],verptr->code[m]); if(substr) mismatch=0; else mismatch=1; } else { ' \
                 'while(1) { if((karptr->pos < avyrecord->pos) && karptr!= NULL && strcmp(karptr->code[0],code2)==0) { substr=strstr(word[karptr->sub_no],avyrecord->code[m]' \
                 '); if(substr) { mismatch=0; karflag--; } else { mismatch=1; un_match=karptr; } } if(strcmpi(karptr->Type,"Noun") !=0) break; else karptr=karptr->next; } }' \
                 ' } } for(i=0;i<j;i++) free(word[i]); } if(Naflag==0) { if(!krdoth) { if(mismatch==0 && karflag==0) { krdsuc=1; ' \
                 'fprintf(rfp,"The Krdavyaya is Semantically Compatible if %s root means %s and subject is %s ",krdavy->stem,krdavy->base[m],srecord->base[n]); } else { ' \
                 'krdsuc=0; fprintf(rfp,"Verb %s is not compatible with subject %s ",verptr->word,srecord->word); if(un_match != NULL) ' \
                 'fprintf(rfp,"if %s is %s ",un_match->dispSpecf,un_match->word); } } } } } } if(verflag==1) { subver=1; while(strcmpi(verptr->specf,"Verb")==0) ' \
                 '{ if(strcmpi(verptr->dispSpecf,"Verb") ==0 || strcmpi(verptr->dispSpecf,"Krdanta") ==0) { for(m=0;m<(verptr->no_base);m++) ' \
                 '{ num_sub=no_vsub; if(verptr->code[m][0] != "\0") { for(n=0;n<srecord->no_base;n++) { num_sub=no_vsub; rewind(cfp); karmatch=NULL; ' \
                 'while( (c=fgetc(cfp)) != eof) { ungetc(c,cfp); fgets(line,150,cfp); if(line[0]=="\n") continue; karptr=krecord; j=0; j=split(line,word); ' \
                 'strncpy(code1,line,2); code1[2]="\0"; strncpy(code2,line+3,2); code2[2]="\0"; if(shaflag==0) { if(strcmp(srecord->code[n],code1)==0) ' \
                 '{ if(strcmp(code2,"00")==0) { if(strcmp(srecord->code[n],code1)==0) { substr=strstr(word[1],verptr->code[m]); if(substr) ' \
                 '{ if(subver) subver=1; else subver=0; } else { subunmatch=srecord; subver=0; } } } ' \
                 'if(strcmp(code2,"00")==0 && (karptr==NULL || no_vsub==0)) { substr=strstr(word[1],verptr->code[m]); if(substr) flag=0; else flag=1; ' \
                 'if(krdflag) { if(!krdsuc && !flag) flag=0; if(krdsuc && !flag) flag=1; if(krdsuc && flag) flag=1; } } else if(krdflag==0 ) ' \
                 '{ while(strcmpi(karptr->specf,"Verb")!=0 && krecord != NULL) { if(strcmp(karptr->code[0],code2)==0 && Saflag==0) ' \
                 '{ substr=strstr(word[karptr->sub_no],verptr->code[m]); if(substr) { karmatch=karptr; num_sub--; } else un_match=karptr; } ' \
                 'if(strcmp(karptr->code[0],code2)==0 && Saflag==1) { substr=strstr(word[karptr->sub_no],verptr->code[m]); ' \
                 'if(substr) { karmatch=karptr; num_sub--; } else un_match=karptr; } karptr=karptr->next; } } else if(krdflag && no_vsub) ' \
                 '{ while(strcmpi(karptr->specf,"Verb") !=0 && krecord != NULL) { if(strcmp(karptr->code[0],code2)==0) { ' \
                 'if((karptr->pos > krdpos && strcmp(krdfirst->specf,"Subject")==0)|| strcmp(krdfirst->specf,"Subject")!=0 ) {' \
                 ' substr=strstr(word[karptr->sub_no],verptr->code[m]); if(substr) { karmatch=karptr; num_sub--; } else un_match=karptr; } } ' \
                 'karptr=karptr->next; } } } } else if(shaflag==1) { ' \
                 'while(strcmpi(karptr->specf,"Verb") !=0 && strcmpi(karptr->specf,"Krdanta") !=0 && strcmpi(karptr->specf,"Krdavyaya") !=0 && krecord != NULL) {' \
                 ' strncpy(code2,line+3,2); code2[2]="\0"; if(strcmp(code2,"00")==0) { if(strcmp(srecord->code[n],code1)==0) { ' \
                 'substr=strstr(word[1],verptr->code[m]); if(substr) { if(subver) subver=1; else { subunmatch=srecord; subver=0; } } else { ' \
                 'subunmatch=srecord; subver=0; } } } if(karptr->sub_no==6 ) { shrvib=fshtptr ; while(strcmp(karptr->word,shrvib->word) !=0) shrvib=shrvib->next; ' \
                 'if(strcmp(code1,shrvib->code[0])==0 && strcmp(code2,shrvib->next->code[0])==0 ) { if(strcmp(word[6],"*")==0) {' \
                 ' karmatch=karptr; num_sub--; } else un_match=karptr; } } else if(karptr->sub_no < 6 && strcmp(srecord->code[n],code1)==0 ) { ' \
                 'if(strcmp(karptr->code[0],code2)==0 && karptr->pos > krdpos ) { substr=strstr(word[karptr->sub_no],verptr->code[m]); if(substr) { ' \
                 'karmatch=karptr; num_sub--; } else un_match=karptr; } } karptr=karptr->next; } } if(strcmp(code2,"00")==0 && Saflag==1) {' \
                 ' subptr=fstptr; while(1) { if(strcmp(subptr->Type,"Noun")==0 && strcmp(subptr->specf,"Instrument")==0 && (subptr->pos == (Sapos -1)) ) {' \
                 ' if(strcmp(subptr->code[n],code1)==0) { substr=strstr(word[1],verptr->code[m]); if(substr) { if(subver) subver=1; else { ' \
                 'subunmatch=srecord; subver=0; } } else { subunmatch=srecord; subver=0; } } } if(subptr->next == NULL) break; else subptr=subptr->next; } } ' \
                 'for(i=0;i<j;i++) free(word[i]); } if(Naflag==0) { if(num_sub==0 && subver) { flag=1; ' \
                 'fprintf(rfp,"The Verb %s is Semantically Compatible With Subject if Verb Root means %s ",verptr->stem,verptr->base[m]); ' \
                 'if(no_vsub) fprintf(rfp,"and %s is %s ",karmatch->specf,karmatch->base[m]); } else if(subver==0) { flag=0; ' \
                 'fprintf(rfp,"The Verb %s is not compatible with the Subject ",verptr->word); } else if(num_sub && subver) { flag=0; ' \
                 'fprintf(rfp,"The Verb %s is not compatible with Subject if %s is %s ",verptr->word,un_match->specf,un_match->stem); } if(krdflag) {' \
                 ' if(krdsuc==1 && flag==1) flag=1; if(krdsuc==0 ||flag==0) flag=0; } } else if(Naflag==1) flag=1; } if(verptr->no_base > 1) { afppos=ftell(afp); ' \
                 'y=Sabdabodha(afp,sfp,rfp,firstptr,sent,flag,y,pos,Saflag,verptr->base[m],m); fseek(afp,afppos,0); pos=ftell(rfp); fseek(rfp,pos,0); } } ' \
                 'if(verptr->no_base == m+1 && verptr->no_base > 1) { while(!feof(afp)) { fgets(line,499,afp); if(line[0]=="-") break; } } } ' \
                 'if(verptr->next==NULL) break; else verptr=verptr->next; } } } srecord=srecord->next; } if(flag==1) ' \
                 'fprintf(rfp,"\nThe Sentence is Semantically Compatible"); else fprintf(rfp,"\nThe Sentence is Semantically Not Compatible"); ' \
                 'fprintf(rfp,"\n-------------------\n"); if(fshtptr != NULL) { shrvib=fshtptr; tshrvib=shrvib; while(fshtptr->next != NULL) {' \
                 ' while(shrvib->next != NULL) { tshrvib=shrvib; shrvib=shrvib->next; } free(shrvib->specf); free(shrvib->word); for(i=0;i<shrvib->no_base;i++) {' \
                 ' free(shrvib->base[i]); free(shrvib->code[i]); } free(shrvib); tshrvib->next=NULL; shrvib=fshtptr; } free(shrvib->specf); free(shrvib->word); ' \
                 'for(i=0;i<fshtptr->no_base;i++) { free(fshtptr->base[i]); free(fshtptr->code[i]); } free(fshtptr); }'
stmt_assignment_double = 'fvibptr=tvibptr=(VIBAK *)malloc(sizeof(VIBAK))'
stmt_assignment_index_plusplus = 'verb[j++]=word[i];'
stmt_function_arg_with_plus_invoke = 'tvibptr->sent=malloc(strlen(sen +1*k)-g);'
stmt_typedef_at_start = "typedef struct detail { char *Type; char *code[20]; char *subcode; unsigned char *specf; unsigned char *dispSpecf; unsigned char *mean_deno; unsigned char *word; unsigned char *stem; unsigned char *base[20]; unsigned char *voice; int linga; int vibvach; int mode; int sub_no; int no_base; int no_codes; int pos; int matnoun; int subinsen; struct detail *next; }DETAIL; "
stmt_typedef_already_defined = "typedef struct vibak VIBAK; typedef struct display DISP_ARTH; typedef struct shasti SHASTI; typedef struct disp_shasti DISPLAY;"
stmt_typedef_no_struct = 'typedef	unsigned char* DEVSTR ;typedef unsigned char  DEVCHR ; #define ANUSVARA (DEVCHR) "¢"'
stmt_expression_type_cast = 'if(message[strlen(message)-1]==(unsigned char) "*") ab = (unsigned char *) bc;'
stmt_char_plusminus_char = '*sp = input[i+1] - (unsigned char)("Ú"-"¥");'
stmt_type_cast_pointer_math = 'strcat(fp,(unsigned char *)"è");if( *(input+i+1)>=(unsigned char)"Ú" && *(input+i+1)<=(unsigned char)"æ");'
stmt_pesky_pointer_array = 'strcpy(sp+1,input+i+2);if(*(input+i) >= (unsigned char)"¤" && *(input+i) <= (unsigned char)"Ø") { if(fp[0] != "\0" && sp[0] != "\0") { splitWords->firstWord[count] = strdup(fp); splitWords->secondWord[count] = strdup(sp); count++; } }'
stmt_split_c_complete = '/**************************************************************** File : SPLIT.C Function : splitTheWord The C code of this function splits the word that is passed to it into right and left strings for all possible combinations. The right and left strings are stored in a structure and is returned by the funtion. NOTE: THE CALLER OF THIS FUNCTION MUST FREE THE MEMORY USED BY THIS STRUCTURE. Function : splitTheSentence The C code of this function splits the sentence that is passed to it into words and are stored in a structure and is returned by the funtion. NOTE: THE CALLER OF THIS FUNCTION MUST FREE THE MEMORY USED BY THIS STRUCTURE. Note that the Options->Compiler->Source Option in the IDE has been set to ANSI-C, to ensure strict adherence to ANSI-C standards. Compilation has been verified to give 0 warnings and 0 errors with this setting. ****************************************************************/; #include <stdio.h> #include <string.h> #include <conio.h> #include <stdlib.h> #include <process.h> #include "senanal.h" SPLIT *splitTheWord(unsigned char *input) { int i,j,len,count; unsigned char fp[100], sp[100]; SPLIT *splitWords, *splitWord; for(i=0;input[i]!= "\0";i++); i=-2 ; strcpy(fp,""); strcpy(sp,""); count=0; splitWords = (SPLIT *) malloc (sizeof(SPLIT)); while(i >= 0) { if(input[i]>=(unsigned char)"¤" && input[i]<=(unsigned char)"±") { strcpy(sp,input+i); for(j=0;j<i;j++) fp[j]=input[j]; fp[j]=0; } else if(input[i]>=(unsigned char)"³" && input[i]<=(unsigned char)"Ø") { if( *(input+i+1)>=(unsigned char)"Ú" && *(input+i+1)<=(unsigned char)"æ") { if(*(input+i+1)>=(unsigned char)"Ú" && *(input+i+1)<=(unsigned char)"ß") *sp = input[i+1] - (unsigned char)("Ú"-"¥"); else if(*(input+i+1)>=(unsigned char)"à" && *(input+i+1)<=(unsigned char)"æ") *sp = input[i+1] - (unsigned char)("à"-"«"); } else if( *(input+i+1) >= (unsigned char)"¤" && *(input+i+1) <=(unsigned char) "Ø" || *(input+i+1) == NULL || *(input+i+1) <= (unsigned char)"£") { *sp=(unsigned char)"¤"; strcpy(sp+1,input+i+1); } else if(*(input+i+1) == (unsigned char)"è") strcpy(sp,input+i+2); for(j=0;j<=i;j++) fp[j]= input[j]; fp[j]=0; strcat(fp,(unsigned char *)"è"); } if(*(input+i) >= (unsigned char)"¤" && *(input+i) <= (unsigned char)"Ø") { if(fp[0] != "\0" && sp[0] != "\0") { splitWords->firstWord[count] = strdup(fp); splitWords->secondWord[count] = strdup(sp); count++; } } /************************** Second Possible Split start ***************************/; if(input[i] >= (unsigned char)"¤" && input[i] <= (unsigned char)"Ø") { for(j=0;j<i;j++) fp[j]=input[j]; fp[j]=0; strcpy(sp,input+i); if(*(input+i) >= (unsigned char)"¤" && *(input+i) <= (unsigned char)"Ø") { if(fp[0] != "\0" && sp[0] != "\0") { splitWords->firstWord[count] = strdup(fp); splitWords->secondWord[count] = strdup(sp); count++; } } } /************************** Second Possible Split end ***************************/; i--; if(count==8) break; } splitWords->noOfSplits = count; splitWord = (SPLIT *) malloc (sizeof(SPLIT)); j = 0; for(i = 0; i < splitWords->noOfSplits; i++) { splitWord->firstWord[j] = (unsigned char *) malloc(strlen(splitWords->firstWord[i]) + 1); strcpy(splitWord->firstWord[j], splitWords->firstWord[i]); splitWord->secondWord[j] = (unsigned char *) malloc(strlen(splitWords->secondWord[i]) + 1); strcpy(splitWord->secondWord[j], splitWords->secondWord[i]); j++; if(strcmp(splitWords->firstWord[i],splitWords->firstWord[i+1]) == 0 && strcmp(splitWords->secondWord[i],splitWords->secondWord[i+1]) == 0) i++; } splitWord->noOfSplits = j; for(i = 0; i < splitWords->noOfSplits; i++) { free(splitWords->firstWord[i]); free(splitWords->secondWord[i]); } free(splitWords); return(splitWord); } /*SPLIT1 *splitTheSentence(unsigned char *record) { int i; SPLIT1 *splitSen; unsigned char *token; splitSen = (SPLIT1 *) malloc(sizeof(SPLIT1)); i = 0; token = strtok(record, " "); splitSen->word[i] = (unsigned char *) malloc(strlen(token) + 1); strcpy(splitSen->word[i], token); i++ ; while (1) { token = strtok(NULL, " ") ; if (token == NULL) break ; splitSen->word[i] = (unsigned char *) malloc(strlen(token) + 1); strcpy(splitSen->word[i], token) ; i++ ; } splitSen->noOfWords = i; return (splitSen); } */;'
samples = [stmt_comment, stmt_var_decl_initialized, stmt_var_decl_array, stmt_assignment, stmt_func_decl_default, stmt_func_decl_complex,
           stmt_func_decl_complex1, stmt_func_decl_complex2, stmt_func_def_complex1, stmt_func_def_complex2, stmt_assignment_func, stmt_if_assign,
           stmt_if_assign2, stmt_if_assign3, stmt_if_assign4, stmt_strcmp_cpy_cat, stmt_switch_case, stmt_switch_case1, stmt_switch_case2,
           stmt_switch_case22, stmt_switch_case3, stmt_while, stmt_if_while_complex1, stmt_while_complex2, stmt_while_complex3, stmt_define, stmt_include,
           stmt_include2, stmt_typedef_many, stmt_func_def_vibmenu_c_complete, stmt_increment_decrement, stmt_for, stmt_func_def_complex3,
           stmt_assignment_and_condition, stmt_multilevel_indices_pointers, stmt_includes_defines_others, stmt_multilevel_pointers_indices_and_assigned_conditions,
           stmt_assignment_double, stmt_assignment_index_plusplus, stmt_function_arg_with_plus_invoke,
           stmt_typedef_at_start, stmt_typedef_already_defined, stmt_typedef_no_struct, stmt_expression_type_cast, stmt_char_plusminus_char,
           stmt_type_cast_pointer_math, stmt_pesky_pointer_array, stmt_split_c_complete]

pattern_crlf, pattern_lf, pattern_spaces_2_or_more, pattern_tabs, \
pattern_c_strcmp, pattern_c_strcpy, pattern_c_strcat, pattern_c_strncpy, pattern_include, pattern_define, \
pattern_end_with_newline, pattern_star_slash, pattern_star_slash_semicolon, pattern_char_plus_minus_char = \
        re.compile(r"\r\n"), re.compile(r"\n"), re.compile(" +"), re.compile("\t+"), \
        re.compile("strcmpi?\((.+?),(.+?)\)\s*([=|!]=)\s*0"), re.compile("strcpy\((.+?)\s*,\s*(.+?)\)"),\
        re.compile("strcat\(\s*(.+?)\s*,\s*(.+?)\s*\)"), re.compile("strncpy\((.+?)\s*,\s*(.+?)(\+?)(\d+?)*\,(\w+)\);\s+\w+\[\d+\]\s*\=\S+;?"), \
        re.compile(r"#include\s+(.+?)\s+"), re.compile(r"#define\s+(.+?)\s+(.+?)\s+\w*"), \
        re.compile(r"\n$"), re.compile(r"\*\/"),  re.compile(r"\*\/;"), re.compile(r'\"(\S?)\"([\+|\-])\"(\S?)\"')