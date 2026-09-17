
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__004ff070(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x150) != '\0') {
    local_c = local_c & 0xffffff00;
    FUN__text__00505000((int)_DAT_00757100,(int)_DAT_00757102,(int)_DAT_00757104,
                        (int)*(short *)(param_1 + 0x180),(int)_DAT_00757108,(int)_DAT_0075710a,
                        (int)_DAT_0075710c,(int)_DAT_0075710e);
  }
  if (*(char *)(local_8 + 0x151) != '\0') {
    local_c._0_1_ = 3;
    FUN__text__00505000((int)_UNK_00757130,(int)_UNK_00757132,(int)_UNK_00757134,
                        (int)*(short *)(local_8 + 0x182),(int)_UNK_00757138,(int)_UNK_0075713a,
                        (int)_UNK_0075713c,(int)_UNK_0075713e);
    local_c = CONCAT31(local_c._1_3_,0x25);
    FUN__text__00505000((int)_UNK_00757350,(int)_UNK_00757352,(int)_UNK_00757354,
                        *(short *)(local_8 + 0x182) + 0x24,(int)_UNK_00757358,(int)_UNK_0075735a,
                        (int)_UNK_0075735c,(int)_UNK_0075735e);
  }
  if (*(char *)(local_8 + 0x152) != '\0') {
    local_c._0_1_ = 4;
    FUN__text__00505000((int)_UNK_00757140,(int)_UNK_00757142,(int)_UNK_00757144,
                        (int)*(short *)(local_8 + 0x184),(int)_UNK_00757148,(int)_UNK_0075714a,
                        (int)_UNK_0075714c,(int)_UNK_0075714e);
    local_c._0_1_ = 0x25;
    FUN__text__00505000((int)_UNK_00757350,(int)_UNK_00757352,(int)_UNK_00757354,
                        *(short *)(local_8 + 0x184) + 0x24,(int)_UNK_00757358,(int)_UNK_0075735a,
                        (int)_UNK_0075735c,(int)_UNK_0075735e);
    local_c = CONCAT31(local_c._1_3_,0x26);
    FUN__text__00505000((int)_UNK_00757360,(int)_UNK_00757362,(int)_UNK_00757364,
                        *(short *)(local_8 + 0x184) + 0x48,(int)_UNK_00757368,(int)_UNK_0075736a,
                        (int)_UNK_0075736c,(int)_UNK_0075736e);
  }
  if (*(char *)(local_8 + 0x153) != '\0') {
    local_c = CONCAT31(local_c._1_3_,0x18);
    FUN__text__00505000((int)_UNK_00757280,(int)_UNK_00757282,(int)_UNK_00757284,
                        (int)*(short *)(local_8 + 0x186),(int)_UNK_00757288,(int)_UNK_0075728a,
                        (int)_UNK_0075728c,(int)_UNK_0075728e);
  }
  if (*(char *)(local_8 + 0x154) != '\0') {
    local_c = CONCAT31(local_c._1_3_,0x20);
    FUN__text__00505000((int)_UNK_00757300,(int)_UNK_00757302,(int)_UNK_00757304,
                        (int)*(short *)(local_8 + 0x188),(int)_UNK_00757308,(int)_UNK_0075730a,
                        (int)_UNK_0075730c,(int)_UNK_0075730e);
  }
  if (*(char *)(local_8 + 0x155) != '\0') {
    local_c._0_1_ = 0x56;
    FUN__text__00505000((int)_UNK_00757660,(int)_UNK_00757662,(int)_UNK_00757664,
                        (int)*(short *)(local_8 + 0x18a),(int)_UNK_00757668,(int)_UNK_0075766a,
                        (int)_UNK_0075766c,(int)_UNK_0075766e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x18a) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x32);
    FUN__text__00505000((int)_UNK_00757420,(int)_UNK_00757422,(int)_UNK_00757424,
                        *(short *)(local_8 + 0x18a) + 0x48,(int)_UNK_00757428,(int)_UNK_0075742a,
                        (int)_UNK_0075742c,(int)_UNK_0075742e);
  }
  if (*(char *)(local_8 + 0x156) != '\0') {
    local_c._0_1_ = 0x5c;
    FUN__text__00505000((int)_UNK_007576c0,(int)_UNK_007576c2,(int)_UNK_007576c4,
                        (int)*(short *)(local_8 + 0x18c),(int)_UNK_007576c8,(int)_UNK_007576ca,
                        (int)_UNK_007576cc,(int)_UNK_007576ce);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x18c) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x33);
    FUN__text__00505000((int)_UNK_00757430,(int)_UNK_00757432,(int)_UNK_00757434,
                        *(short *)(local_8 + 0x18c) + 0x48,(int)_UNK_00757438,(int)_UNK_0075743a,
                        (int)_UNK_0075743c,(int)_UNK_0075743e);
  }
  if (*(char *)(local_8 + 0x157) != '\0') {
    local_c._0_1_ = 0x5d;
    FUN__text__00505000((int)_UNK_007576d0,(int)_UNK_007576d2,(int)_UNK_007576d4,
                        (int)*(short *)(local_8 + 0x18e),(int)_UNK_007576d8,(int)_UNK_007576da,
                        (int)_UNK_007576dc,(int)_UNK_007576de);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x18e) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x34);
    FUN__text__00505000((int)_UNK_00757440,(int)_UNK_00757442,(int)_UNK_00757444,
                        *(short *)(local_8 + 0x18e) + 0x48,(int)_UNK_00757448,(int)_UNK_0075744a,
                        (int)_UNK_0075744c,(int)_UNK_0075744e);
  }
  if (*(char *)(local_8 + 0x158) != '\0') {
    local_c._0_1_ = 0x5f;
    FUN__text__00505000((int)_UNK_007576f0,(int)_UNK_007576f2,(int)_UNK_007576f4,
                        (int)*(short *)(local_8 + 400),(int)_UNK_007576f8,(int)_UNK_007576fa,
                        (int)_UNK_007576fc,(int)_UNK_007576fe);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 400) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x35);
    FUN__text__00505000((int)_UNK_00757450,(int)_UNK_00757452,(int)_UNK_00757454,
                        *(short *)(local_8 + 400) + 0x48,(int)_UNK_00757458,(int)_UNK_0075745a,
                        (int)_UNK_0075745c,(int)_UNK_0075745e);
  }
  if (*(char *)(local_8 + 0x159) != '\0') {
    local_c._0_1_ = 0x58;
    FUN__text__00505000((int)_UNK_00757680,(int)_UNK_00757682,(int)_UNK_00757684,
                        (int)*(short *)(local_8 + 0x192),(int)_UNK_00757688,(int)_UNK_0075768a,
                        (int)_UNK_0075768c,(int)_UNK_0075768e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x192) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x36);
    FUN__text__00505000((int)_UNK_00757460,(int)_UNK_00757462,(int)_UNK_00757464,
                        *(short *)(local_8 + 0x192) + 0x48,(int)_UNK_00757468,(int)_UNK_0075746a,
                        (int)_UNK_0075746c,(int)_UNK_0075746e);
  }
  if (*(char *)(local_8 + 0x15a) != '\0') {
    local_c._0_1_ = 0x5a;
    FUN__text__00505000((int)_UNK_007576a0,(int)_UNK_007576a2,(int)_UNK_007576a4,
                        (int)*(short *)(local_8 + 0x194),(int)_UNK_007576a8,(int)_UNK_007576aa,
                        (int)_UNK_007576ac,(int)_UNK_007576ae);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x194) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x37);
    FUN__text__00505000((int)_UNK_00757470,(int)_UNK_00757472,(int)_UNK_00757474,
                        *(short *)(local_8 + 0x194) + 0x48,(int)_UNK_00757478,(int)_UNK_0075747a,
                        (int)_UNK_0075747c,(int)_UNK_0075747e);
  }
  if (*(char *)(local_8 + 0x15b) != '\0') {
    local_c._0_1_ = 0x5e;
    FUN__text__00505000((int)_UNK_007576e0,(int)_UNK_007576e2,(int)_UNK_007576e4,
                        (int)*(short *)(local_8 + 0x196),(int)_UNK_007576e8,(int)_UNK_007576ea,
                        (int)_UNK_007576ec,(int)_UNK_007576ee);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x196) + 0x2a,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x38);
    FUN__text__00505000((int)_UNK_00757480,(int)_UNK_00757482,(int)_UNK_00757484,
                        *(short *)(local_8 + 0x196) + 0x47,(int)_UNK_00757488,(int)_UNK_0075748a,
                        (int)_UNK_0075748c,(int)_UNK_0075748e);
  }
  if (*(char *)(local_8 + 0x15c) != '\0') {
    local_c._0_1_ = 0x5b;
    FUN__text__00505000((int)_UNK_007576b0,(int)_UNK_007576b2,(int)_UNK_007576b4,
                        (int)*(short *)(local_8 + 0x198),(int)_UNK_007576b8,(int)_UNK_007576ba,
                        (int)_UNK_007576bc,(int)_UNK_007576be);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x198) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x39);
    FUN__text__00505000((int)_UNK_00757490,(int)_UNK_00757492,(int)_UNK_00757494,
                        *(short *)(local_8 + 0x198) + 0x48,(int)_UNK_00757498,(int)_UNK_0075749a,
                        (int)_UNK_0075749c,(int)_UNK_0075749e);
  }
  if (*(char *)(local_8 + 0x15d) != '\0') {
    local_c._0_1_ = 0x60;
    FUN__text__00505000((int)_UNK_00757700,(int)_UNK_00757702,(int)_UNK_00757704,
                        (int)*(short *)(local_8 + 0x19a),(int)_UNK_00757708,(int)_UNK_0075770a,
                        (int)_UNK_0075770c,(int)_UNK_0075770e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x19a) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x3a);
    FUN__text__00505000((int)_UNK_007574a0,(int)_UNK_007574a2,(int)_UNK_007574a4,
                        *(short *)(local_8 + 0x19a) + 0x48,(int)_UNK_007574a8,(int)_UNK_007574aa,
                        (int)_UNK_007574ac,(int)_UNK_007574ae);
  }
  if (*(char *)(local_8 + 0x15e) != '\0') {
    local_c._0_1_ = 0x61;
    FUN__text__00505000((int)_UNK_00757710,(int)_UNK_00757712,(int)_UNK_00757714,
                        (int)*(short *)(local_8 + 0x19c),(int)_UNK_00757718,(int)_UNK_0075771a,
                        (int)_UNK_0075771c,(int)_UNK_0075771e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x19c) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x3b);
    FUN__text__00505000((int)_UNK_007574b0,(int)_UNK_007574b2,(int)_UNK_007574b4,
                        *(short *)(local_8 + 0x19c) + 0x49,(int)_UNK_007574b8,(int)_UNK_007574ba,
                        (int)_UNK_007574bc,(int)_UNK_007574be);
  }
  if (*(char *)(local_8 + 0x15f) != '\0') {
    local_c._0_1_ = 0x59;
    FUN__text__00505000((int)_UNK_00757690,(int)_UNK_00757692,(int)_UNK_00757694,
                        (int)*(short *)(local_8 + 0x19e),(int)_UNK_00757698,(int)_UNK_0075769a,
                        (int)_UNK_0075769c,(int)_UNK_0075769e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x19e) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x3c);
    FUN__text__00505000((int)_UNK_007574c0,(int)_UNK_007574c2,(int)_UNK_007574c4,
                        *(short *)(local_8 + 0x19e) + 0x48,(int)_UNK_007574c8,(int)_UNK_007574ca,
                        (int)_UNK_007574cc,(int)_UNK_007574ce);
  }
  if (*(char *)(local_8 + 0x160) != '\0') {
    local_c._0_1_ = 0x57;
    FUN__text__00505000((int)_UNK_00757670,(int)_UNK_00757672,(int)_UNK_00757674,
                        (int)*(short *)(local_8 + 0x1a0),(int)_UNK_00757678,(int)_UNK_0075767a,
                        (int)_UNK_0075767c,(int)_UNK_0075767e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x1a0) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x3d);
    FUN__text__00505000((int)_UNK_007574d0,(int)_UNK_007574d2,(int)_UNK_007574d4,
                        *(short *)(local_8 + 0x1a0) + 0x48,(int)_UNK_007574d8,(int)_UNK_007574da,
                        (int)_UNK_007574dc,(int)_UNK_007574de);
  }
  if (*(char *)(local_8 + 0x161) != '\0') {
    local_c._0_1_ = 0x62;
    FUN__text__00505000((int)_UNK_00757720,(int)_UNK_00757722,(int)_UNK_00757724,
                        (int)*(short *)(local_8 + 0x1a2),(int)_UNK_00757728,(int)_UNK_0075772a,
                        (int)_UNK_0075772c,(int)_UNK_0075772e);
    local_c._0_1_ = 0x68;
    FUN__text__00505000((int)_UNK_00757780,(int)_UNK_00757782,(int)_UNK_00757784,
                        *(short *)(local_8 + 0x1a2) + 0x2b,(int)_UNK_00757788,(int)_UNK_0075778a,
                        (int)_UNK_0075778c,(int)_UNK_0075778e);
    local_c = CONCAT31(local_c._1_3_,0x3e);
    FUN__text__00505000((int)_UNK_007574e0,(int)_UNK_007574e2,(int)_UNK_007574e4,
                        *(short *)(local_8 + 0x1a2) + 0x48,(int)_UNK_007574e8,(int)_UNK_007574ea,
                        (int)_UNK_007574ec,(int)_UNK_007574ee);
  }
  if (*(char *)(local_8 + 0x162) != '\0') {
    local_c = CONCAT31(local_c._1_3_,0x21);
    FUN__text__00505000((int)_UNK_00757310,(int)_UNK_00757312,(int)_UNK_00757314,
                        (int)*(short *)(local_8 + 0x1a4),(int)_UNK_00757318,(int)_UNK_0075731a,
                        (int)_UNK_0075731c,(int)_UNK_0075731e);
  }
  if (*(char *)(local_8 + 0x163) != '\0') {
    local_c._0_1_ = 99;
    FUN__text__00505000((int)_UNK_00757730,(int)_UNK_00757732,(int)_UNK_00757734,
                        (int)*(short *)(local_8 + 0x1a6),(int)_UNK_00757738,(int)_UNK_0075773a,
                        (int)_UNK_0075773c,(int)_UNK_0075773e);
    local_c._0_1_ = 100;
    FUN__text__00505000((int)_UNK_00757740,(int)_UNK_00757742,(int)_UNK_00757744,
                        *(short *)(local_8 + 0x1a6) + 0x24,(int)_UNK_00757748,(int)_UNK_0075774a,
                        (int)_UNK_0075774c,(int)_UNK_0075774e);
    local_c._0_1_ = 0x65;
    FUN__text__00505000((int)_UNK_00757750,(int)_UNK_00757752,(int)_UNK_00757754,
                        *(short *)(local_8 + 0x1a6) + 0x48,(int)_UNK_00757758,(int)_UNK_0075775a,
                        (int)_UNK_0075775c,(int)_UNK_0075775e);
    local_c._0_1_ = 0x66;
    FUN__text__00505000((int)_UNK_00757760,(int)_UNK_00757762,(int)_UNK_00757764,
                        *(short *)(local_8 + 0x1a6) + 0x6d,(int)_UNK_00757768,(int)_UNK_0075776a,
                        (int)_UNK_0075776c,(int)_UNK_0075776e);
    local_c = CONCAT31(local_c._1_3_,0x67);
    FUN__text__00505000((int)_UNK_00757770,(int)_UNK_00757772,(int)_UNK_00757774,
                        *(short *)(local_8 + 0x1a6) + 0x90,(int)_UNK_00757778,(int)_UNK_0075777a,
                        (int)_UNK_0075777c,(int)_UNK_0075777e);
  }
  if (*(char *)(local_8 + 0x164) != '\0') {
    local_c._0_1_ = 0x19;
    FUN__text__00505000((int)_UNK_00757290,(int)_UNK_00757292,(int)_UNK_00757294,
                        (int)*(short *)(local_8 + 0x1a8),(int)_UNK_00757298,(int)_UNK_0075729a,
                        (int)_UNK_0075729c,(int)_UNK_0075729e);
    local_c = CONCAT31(local_c._1_3_,0x30);
    FUN__text__00505000((int)_UNK_00757400,(int)_UNK_00757402,(int)_UNK_00757404,
                        *(short *)(local_8 + 0x1a8) + 0x24,(int)_UNK_00757408,(int)_UNK_0075740a,
                        (int)_UNK_0075740c,(int)_UNK_0075740e);
  }
  if (*(char *)(local_8 + 0x165) != '\0') {
    local_c._0_1_ = 5;
    FUN__text__00505000((int)_UNK_00757150,(int)_UNK_00757152,(int)_UNK_00757154,
                        (int)*(short *)(local_8 + 0x1aa),(int)_UNK_00757158,(int)_UNK_0075715a,
                        (int)_UNK_0075715c,(int)_UNK_0075715e);
    local_c = CONCAT31(local_c._1_3_,0x27);
    FUN__text__00505000((int)_UNK_00757370,(int)_UNK_00757372,(int)_UNK_00757374,
                        *(short *)(local_8 + 0x1aa) + 0x24,(int)_UNK_00757378,(int)_UNK_0075737a,
                        (int)_UNK_0075737c,(int)_UNK_0075737e);
  }
  if (*(char *)(local_8 + 0x166) != '\0') {
    local_c._0_1_ = 8;
    FUN__text__00505000((int)_UNK_00757180,(int)_UNK_00757182,(int)_UNK_00757184,
                        (int)*(short *)(local_8 + 0x1ac),(int)_UNK_00757188,(int)_UNK_0075718a,
                        (int)_UNK_0075718c,(int)_UNK_0075718e);
    local_c = CONCAT31(local_c._1_3_,0x28);
    FUN__text__00505000((int)_UNK_00757380,(int)_UNK_00757382,(int)_UNK_00757384,
                        *(short *)(local_8 + 0x1ac) + 0x24,(int)_UNK_00757388,(int)_UNK_0075738a,
                        (int)_UNK_0075738c,(int)_UNK_0075738e);
  }
  if (*(char *)(local_8 + 0x167) != '\0') {
    local_c._0_1_ = 9;
    FUN__text__00505000((int)_UNK_00757190,(int)_UNK_00757192,(int)_UNK_00757194,
                        (int)*(short *)(local_8 + 0x1ae),(int)_UNK_00757198,(int)_UNK_0075719a,
                        (int)_UNK_0075719c,(int)_UNK_0075719e);
    local_c = CONCAT31(local_c._1_3_,0x29);
    FUN__text__00505000((int)_UNK_00757390,(int)_UNK_00757392,(int)_UNK_00757394,
                        *(short *)(local_8 + 0x1ae) + 0x24,(int)_UNK_00757398,(int)_UNK_0075739a,
                        (int)_UNK_0075739c,(int)_UNK_0075739e);
  }
  if (*(char *)(local_8 + 0x168) != '\0') {
    local_c._0_1_ = 7;
    FUN__text__00505000((int)_UNK_00757170,(int)_UNK_00757172,(int)_UNK_00757174,
                        (int)*(short *)(local_8 + 0x1b0),(int)_UNK_00757178,(int)_UNK_0075717a,
                        (int)_UNK_0075717c,(int)_UNK_0075717e);
    local_c = CONCAT31(local_c._1_3_,0x27);
    FUN__text__00505000((int)_UNK_00757370,(int)_UNK_00757372,(int)_UNK_00757374,
                        *(short *)(local_8 + 0x1b0) + 0x24,(int)_UNK_00757378,(int)_UNK_0075737a,
                        (int)_UNK_0075737c,(int)_UNK_0075737e);
  }
  if (*(char *)(local_8 + 0x169) != '\0') {
    local_c._0_1_ = 6;
    FUN__text__00505000((int)_UNK_00757160,(int)_UNK_00757162,(int)_UNK_00757164,
                        (int)*(short *)(local_8 + 0x1b2),(int)_UNK_00757168,(int)_UNK_0075716a,
                        (int)_UNK_0075716c,(int)_UNK_0075716e);
    local_c = CONCAT31(local_c._1_3_,0x28);
    FUN__text__00505000((int)_UNK_00757380,(int)_UNK_00757382,(int)_UNK_00757384,
                        *(short *)(local_8 + 0x1b2) + 0x24,(int)_UNK_00757388,(int)_UNK_0075738a,
                        (int)_UNK_0075738c,(int)_UNK_0075738e);
  }
  if (*(char *)(local_8 + 0x16a) != '\0') {
    local_c._0_1_ = 0x13;
    FUN__text__00505000((int)_UNK_00757230,(int)_UNK_00757232,(int)_UNK_00757234,
                        (int)*(short *)(local_8 + 0x1b4),(int)_UNK_00757238,(int)_UNK_0075723a,
                        (int)_UNK_0075723c,(int)_UNK_0075723e);
    local_c = CONCAT31(local_c._1_3_,0x25);
    FUN__text__00505000((int)_UNK_00757350,(int)_UNK_00757352,(int)_UNK_00757354,
                        *(short *)(local_8 + 0x1b4) + 0x24,(int)_UNK_00757358,(int)_UNK_0075735a,
                        (int)_UNK_0075735c,(int)_UNK_0075735e);
  }
  if (*(char *)(local_8 + 0x16b) != '\0') {
    local_c._0_1_ = 0x14;
    FUN__text__00505000((int)_UNK_00757240,(int)_UNK_00757242,(int)_UNK_00757244,
                        (int)*(short *)(local_8 + 0x1b6),(int)_UNK_00757248,(int)_UNK_0075724a,
                        (int)_UNK_0075724c,(int)_UNK_0075724e);
    local_c._0_1_ = 0x29;
    FUN__text__00505000((int)_UNK_00757390,(int)_UNK_00757392,(int)_UNK_00757394,
                        *(short *)(local_8 + 0x1b6) + 0x24,(int)_UNK_00757398,(int)_UNK_0075739a,
                        (int)_UNK_0075739c,(int)_UNK_0075739e);
    local_c._0_1_ = 0x26;
    FUN__text__00505000((int)_UNK_00757360,(int)_UNK_00757362,(int)_UNK_00757364,
                        *(short *)(local_8 + 0x1b6) + 0x48,(int)_UNK_00757368,(int)_UNK_0075736a,
                        (int)_UNK_0075736c,(int)_UNK_0075736e);
    local_c = CONCAT31(local_c._1_3_,0x2c);
    FUN__text__00505000((int)_UNK_007573c0,(int)_UNK_007573c2,(int)_UNK_007573c4,
                        *(short *)(local_8 + 0x1b6) + 0x6c,(int)_UNK_007573c8,(int)_UNK_007573ca,
                        (int)_UNK_007573cc,(int)_UNK_007573ce);
  }
  if (*(char *)(local_8 + 0x16c) != '\0') {
    local_c._0_1_ = 0xf;
    FUN__text__00505000((int)_UNK_007571f0,(int)_UNK_007571f2,(int)_UNK_007571f4,
                        (int)*(short *)(local_8 + 0x1b8),(int)_UNK_007571f8,(int)_UNK_007571fa,
                        (int)_UNK_007571fc,(int)_UNK_007571fe);
    local_c = CONCAT31(local_c._1_3_,0x2c);
    FUN__text__00505000((int)_UNK_007573c0,(int)_UNK_007573c2,(int)_UNK_007573c4,
                        *(short *)(local_8 + 0x1b8) + 0x24,(int)_UNK_007573c8,(int)_UNK_007573ca,
                        (int)_UNK_007573cc,(int)_UNK_007573ce);
  }
  if (*(char *)(local_8 + 0x16d) != '\0') {
    local_c._0_1_ = 0xc;
    FUN__text__00505000((int)_UNK_007571c0,(int)_UNK_007571c2,(int)_UNK_007571c4,
                        (int)*(short *)(local_8 + 0x1ba),(int)_UNK_007571c8,(int)_UNK_007571ca,
                        (int)_UNK_007571cc,(int)_UNK_007571ce);
    local_c = CONCAT31(local_c._1_3_,0x2b);
    FUN__text__00505000((int)_UNK_007573b0,(int)_UNK_007573b2,(int)_UNK_007573b4,
                        *(short *)(local_8 + 0x1ba) + 0x24,(int)_UNK_007573b8,(int)_UNK_007573ba,
                        (int)_UNK_007573bc,(int)_UNK_007573be);
  }
  if (*(char *)(local_8 + 0x16e) != '\0') {
    local_c._0_1_ = 0xe;
    FUN__text__00505000((int)_UNK_007571e0,(int)_UNK_007571e2,(int)_UNK_007571e4,
                        (int)*(short *)(local_8 + 0x1bc),(int)_UNK_007571e8,(int)_UNK_007571ea,
                        (int)_UNK_007571ec,(int)_UNK_007571ee);
    local_c = CONCAT31(local_c._1_3_,0x26);
    FUN__text__00505000((int)_UNK_00757360,(int)_UNK_00757362,(int)_UNK_00757364,
                        *(short *)(local_8 + 0x1bc) + 0x24,(int)_UNK_00757368,(int)_UNK_0075736a,
                        (int)_UNK_0075736c,(int)_UNK_0075736e);
  }
  if (*(char *)(local_8 + 0x16f) != '\0') {
    local_c._0_1_ = 0x10;
    FUN__text__00505000((int)_UNK_00757200,(int)_UNK_00757202,(int)_UNK_00757204,
                        (int)*(short *)(local_8 + 0x1be),(int)_UNK_00757208,(int)_UNK_0075720a,
                        (int)_UNK_0075720c,(int)_UNK_0075720e);
    local_c = CONCAT31(local_c._1_3_,0x2c);
    FUN__text__00505000((int)_UNK_007573c0,(int)_UNK_007573c2,(int)_UNK_007573c4,
                        *(short *)(local_8 + 0x1be) + 0x24,(int)_UNK_007573c8,(int)_UNK_007573ca,
                        (int)_UNK_007573cc,(int)_UNK_007573ce);
  }
  if (*(char *)(local_8 + 0x170) != '\0') {
    local_c._0_1_ = 0x11;
    FUN__text__00505000((int)_UNK_00757210,(int)_UNK_00757212,(int)_UNK_00757214,
                        (int)*(short *)(local_8 + 0x1c0),(int)_UNK_00757218,(int)_UNK_0075721a,
                        (int)_UNK_0075721c,(int)_UNK_0075721e);
    local_c._0_1_ = 0x2d;
    FUN__text__00505000((int)_UNK_007573d0,(int)_UNK_007573d2,(int)_UNK_007573d4,
                        *(short *)(local_8 + 0x1c0) + 0x24,(int)_UNK_007573d8,(int)_UNK_007573da,
                        (int)_UNK_007573dc,(int)_UNK_007573de);
    local_c = CONCAT31(local_c._1_3_,0x2c);
    FUN__text__00505000((int)_UNK_007573c0,(int)_UNK_007573c2,(int)_UNK_007573c4,
                        *(short *)(local_8 + 0x1c0) + 0x48,(int)_UNK_007573c8,(int)_UNK_007573ca,
                        (int)_UNK_007573cc,(int)_UNK_007573ce);
  }
  if (*(char *)(local_8 + 0x171) != '\0') {
    local_c._0_1_ = 0xd;
    FUN__text__00505000((int)_UNK_007571d0,(int)_UNK_007571d2,(int)_UNK_007571d4,
                        (int)*(short *)(local_8 + 0x1c2),(int)_UNK_007571d8,(int)_UNK_007571da,
                        (int)_UNK_007571dc,(int)_UNK_007571de);
    local_c = CONCAT31(local_c._1_3_,0x2b);
    FUN__text__00505000((int)_UNK_007573b0,(int)_UNK_007573b2,(int)_UNK_007573b4,
                        *(short *)(local_8 + 0x1c2) + 0x24,(int)_UNK_007573b8,(int)_UNK_007573ba,
                        (int)_UNK_007573bc,(int)_UNK_007573be);
  }
  if (*(char *)(local_8 + 0x172) != '\0') {
    local_c._0_1_ = 0xb;
    FUN__text__00505000((int)_UNK_007571b0,(int)_UNK_007571b2,(int)_UNK_007571b4,
                        (int)*(short *)(local_8 + 0x1c4),(int)_UNK_007571b8,(int)_UNK_007571ba,
                        (int)_UNK_007571bc,(int)_UNK_007571be);
    local_c = CONCAT31(local_c._1_3_,0x29);
    FUN__text__00505000((int)_UNK_00757390,(int)_UNK_00757392,(int)_UNK_00757394,
                        *(short *)(local_8 + 0x1c4) + 0x24,(int)_UNK_00757398,(int)_UNK_0075739a,
                        (int)_UNK_0075739c,(int)_UNK_0075739e);
  }
  if (*(char *)(local_8 + 0x173) != '\0') {
    local_c._0_1_ = 10;
    FUN__text__00505000((int)_UNK_007571a0,(int)_UNK_007571a2,(int)_UNK_007571a4,
                        (int)*(short *)(local_8 + 0x1c6),(int)_UNK_007571a8,(int)_UNK_007571aa,
                        (int)_UNK_007571ac,(int)_UNK_007571ae);
    local_c = CONCAT31(local_c._1_3_,0x2a);
    FUN__text__00505000((int)_UNK_007573a0,(int)_UNK_007573a2,(int)_UNK_007573a4,
                        *(short *)(local_8 + 0x1c6) + 0x24,(int)_UNK_007573a8,(int)_UNK_007573aa,
                        (int)_UNK_007573ac,(int)_UNK_007573ae);
  }
  if (*(char *)(local_8 + 0x174) != '\0') {
    local_c._0_1_ = 0x15;
    FUN__text__00505000((int)_UNK_00757250,(int)_UNK_00757252,(int)_UNK_00757254,
                        (int)*(short *)(local_8 + 0x1c8),(int)_UNK_00757258,(int)_UNK_0075725a,
                        (int)_UNK_0075725c,(int)_UNK_0075725e);
    local_c = CONCAT31(local_c._1_3_,0x2e);
    FUN__text__00505000((int)_UNK_007573e0,(int)_UNK_007573e2,(int)_UNK_007573e4,
                        *(short *)(local_8 + 0x1c8) + 0x24,(int)_UNK_007573e8,(int)_UNK_007573ea,
                        (int)_UNK_007573ec,(int)_UNK_007573ee);
  }
  if (*(char *)(local_8 + 0x175) != '\0') {
    local_c._0_1_ = 0x12;
    FUN__text__00505000((int)_UNK_00757220,(int)_UNK_00757222,(int)_UNK_00757224,
                        (int)*(short *)(local_8 + 0x1ca),(int)_UNK_00757228,(int)_UNK_0075722a,
                        (int)_UNK_0075722c,(int)_UNK_0075722e);
    local_c._0_1_ = 0x2d;
    FUN__text__00505000((int)_UNK_007573d0,(int)_UNK_007573d2,(int)_UNK_007573d4,
                        *(short *)(local_8 + 0x1ca) + 0x24,(int)_UNK_007573d8,(int)_UNK_007573da,
                        (int)_UNK_007573dc,(int)_UNK_007573de);
    local_c = CONCAT31(local_c._1_3_,0x2c);
    FUN__text__00505000((int)_UNK_007573c0,(int)_UNK_007573c2,(int)_UNK_007573c4,
                        *(short *)(local_8 + 0x1ca) + 0x48,(int)_UNK_007573c8,(int)_UNK_007573ca,
                        (int)_UNK_007573cc,(int)_UNK_007573ce);
  }
  if (*(char *)(local_8 + 0x176) != '\0') {
    local_c._0_1_ = 0x16;
    FUN__text__00505000((int)_UNK_00757260,(int)_UNK_00757262,(int)_UNK_00757264,
                        (int)*(short *)(local_8 + 0x1cc),(int)_UNK_00757268,(int)_UNK_0075726a,
                        (int)_UNK_0075726c,(int)_UNK_0075726e);
    local_c = CONCAT31(local_c._1_3_,0x2f);
    FUN__text__00505000((int)_UNK_007573f0,(int)_UNK_007573f2,(int)_UNK_007573f4,
                        *(short *)(local_8 + 0x1cc) + 0x24,(int)_UNK_007573f8,(int)_UNK_007573fa,
                        (int)_UNK_007573fc,(int)_UNK_007573fe);
  }
  if (*(char *)(local_8 + 0x177) != '\0') {
    local_c._0_1_ = 0x17;
    FUN__text__00505000((int)_UNK_00757270,(int)_UNK_00757272,(int)_UNK_00757274,
                        (int)*(short *)(local_8 + 0x1ce),(int)_UNK_00757278,(int)_UNK_0075727a,
                        (int)_UNK_0075727c,(int)_UNK_0075727e);
    local_c._0_1_ = 0x30;
    FUN__text__00505000((int)_UNK_00757400,(int)_UNK_00757402,(int)_UNK_00757404,
                        *(short *)(local_8 + 0x1ce) + 0x24,(int)_UNK_00757408,(int)_UNK_0075740a,
                        (int)_UNK_0075740c,(int)_UNK_0075740e);
    local_c = CONCAT31(local_c._1_3_,0x31);
    FUN__text__00505000((int)_UNK_00757410,(int)_UNK_00757412,(int)_UNK_00757414,
                        *(short *)(local_8 + 0x1ce) + 0x48,(int)_UNK_00757418,(int)_UNK_0075741a,
                        (int)_UNK_0075741c,(int)_UNK_0075741e);
  }
  if (*(char *)(local_8 + 0x178) != '\0') {
    local_c._0_1_ = 0x1a;
    FUN__text__00505000((int)_UNK_007572a0,(int)_UNK_007572a2,(int)_UNK_007572a4,
                        (int)*(short *)(local_8 + 0x1d0),(int)_UNK_007572a8,(int)_UNK_007572aa,
                        (int)_UNK_007572ac,(int)_UNK_007572ae);
    local_c._0_1_ = 0x3f;
    FUN__text__00505000((int)_UNK_007574f0,(int)_UNK_007574f2,(int)_UNK_007574f4,
                        *(short *)(local_8 + 0x1d0) + 0x24,(int)_UNK_007574f8,(int)_UNK_007574fa,
                        (int)_UNK_007574fc,(int)_UNK_007574fe);
    local_c._0_1_ = 0x40;
    FUN__text__00505000((int)_UNK_00757500,(int)_UNK_00757502,(int)_UNK_00757504,
                        *(short *)(local_8 + 0x1d0) + 0x48,(int)_UNK_00757508,(int)_UNK_0075750a,
                        (int)_UNK_0075750c,(int)_UNK_0075750e);
    local_c._0_1_ = 0x41;
    FUN__text__00505000((int)_UNK_00757510,(int)_UNK_00757512,(int)_UNK_00757514,
                        *(short *)(local_8 + 0x1d0) + 0x6c,(int)_UNK_00757518,(int)_UNK_0075751a,
                        (int)_UNK_0075751c,(int)_UNK_0075751e);
    local_c._0_1_ = 0x42;
    FUN__text__00505000((int)_UNK_00757520,(int)_UNK_00757522,(int)_UNK_00757524,
                        *(short *)(local_8 + 0x1d0) + 0x90,(int)_UNK_00757528,(int)_UNK_0075752a,
                        (int)_UNK_0075752c,(int)_UNK_0075752e);
    local_c._0_1_ = 0x43;
    FUN__text__00505000((int)_UNK_00757530,(int)_UNK_00757532,(int)_UNK_00757534,
                        *(short *)(local_8 + 0x1d0) + 0xb4,(int)_UNK_00757538,(int)_UNK_0075753a,
                        (int)_UNK_0075753c,(int)_UNK_0075753e);
    local_c._0_1_ = 0x44;
    FUN__text__00505000((int)_UNK_00757540,(int)_UNK_00757542,(int)_UNK_00757544,
                        *(short *)(local_8 + 0x1d0) + 0xd8,(int)_UNK_00757548,(int)_UNK_0075754a,
                        (int)_UNK_0075754c,(int)_UNK_0075754e);
    local_c._0_1_ = 0x45;
    FUN__text__00505000((int)_UNK_00757550,(int)_UNK_00757552,(int)_UNK_00757554,
                        *(short *)(local_8 + 0x1d0) + 0xfc,(int)_UNK_00757558,(int)_UNK_0075755a,
                        (int)_UNK_0075755c,(int)_UNK_0075755e);
    local_c = CONCAT31(local_c._1_3_,0x46);
    FUN__text__00505000((int)_UNK_00757560,(int)_UNK_00757562,(int)_UNK_00757564,
                        *(short *)(local_8 + 0x1d0) + 0x120,(int)_UNK_00757568,(int)_UNK_0075756a,
                        (int)_UNK_0075756c,(int)_UNK_0075756e);
  }
  if (*(char *)(local_8 + 0x179) != '\0') {
    local_c._0_1_ = 0x1b;
    FUN__text__00505000((int)_UNK_007572b0,(int)_UNK_007572b2,(int)_UNK_007572b4,
                        (int)*(short *)(local_8 + 0x1d2),(int)_UNK_007572b8,(int)_UNK_007572ba,
                        (int)_UNK_007572bc,(int)_UNK_007572be);
    local_c = CONCAT31(local_c._1_3_,0x47);
    FUN__text__00505000((int)_UNK_00757570,(int)_UNK_00757572,(int)_UNK_00757574,
                        *(short *)(local_8 + 0x1d2) + 0x24,(int)_UNK_00757578,(int)_UNK_0075757a,
                        (int)_UNK_0075757c,(int)_UNK_0075757e);
  }
  if (*(char *)(local_8 + 0x17a) != '\0') {
    local_c._0_1_ = 0x1c;
    FUN__text__00505000((int)_UNK_007572c0,(int)_UNK_007572c2,(int)_UNK_007572c4,
                        (int)*(short *)(local_8 + 0x1d4),(int)_UNK_007572c8,(int)_UNK_007572ca,
                        (int)_UNK_007572cc,(int)_UNK_007572ce);
    local_c._0_1_ = 0x48;
    FUN__text__00505000((int)_UNK_00757580,(int)_UNK_00757582,(int)_UNK_00757584,
                        *(short *)(local_8 + 0x1d4) + 0x24,(int)_UNK_00757588,(int)_UNK_0075758a,
                        (int)_UNK_0075758c,(int)_UNK_0075758e);
    local_c = CONCAT31(local_c._1_3_,0x49);
    FUN__text__00505000((int)_UNK_00757590,(int)_UNK_00757592,(int)_UNK_00757594,
                        *(short *)(local_8 + 0x1d4) + 0x48,(int)_UNK_00757598,(int)_UNK_0075759a,
                        (int)_UNK_0075759c,(int)_UNK_0075759e);
  }
  if (*(char *)(local_8 + 0x17b) != '\0') {
    local_c._0_1_ = 0x1d;
    FUN__text__00505000((int)_UNK_007572d0,(int)_UNK_007572d2,(int)_UNK_007572d4,
                        (int)*(short *)(local_8 + 0x1d6),(int)_UNK_007572d8,(int)_UNK_007572da,
                        (int)_UNK_007572dc,(int)_UNK_007572de);
    local_c = CONCAT31(local_c._1_3_,0x4a);
    FUN__text__00505000((int)_UNK_007575a0,(int)_UNK_007575a2,(int)_UNK_007575a4,
                        *(short *)(local_8 + 0x1d6) + 0x24,(int)_UNK_007575a8,(int)_UNK_007575aa,
                        (int)_UNK_007575ac,(int)_UNK_007575ae);
  }
  if (*(char *)(local_8 + 0x17c) != '\0') {
    local_c._0_1_ = 0x1e;
    FUN__text__00505000((int)_UNK_007572e0,(int)_UNK_007572e2,(int)_UNK_007572e4,
                        (int)*(short *)(local_8 + 0x1d8),(int)_UNK_007572e8,(int)_UNK_007572ea,
                        (int)_UNK_007572ec,(int)_UNK_007572ee);
    local_c = CONCAT31(local_c._1_3_,0x4b);
    FUN__text__00505000((int)_UNK_007575b0,(int)_UNK_007575b2,(int)_UNK_007575b4,
                        *(short *)(local_8 + 0x1d8) + 0x24,(int)_UNK_007575b8,(int)_UNK_007575ba,
                        (int)_UNK_007575bc,(int)_UNK_007575be);
  }
  if (*(char *)(local_8 + 0x17d) != '\0') {
    local_c._0_1_ = 0x1f;
    FUN__text__00505000((int)_UNK_007572f0,(int)_UNK_007572f2,(int)_UNK_007572f4,
                        (int)*(short *)(local_8 + 0x1da),(int)_UNK_007572f8,(int)_UNK_007572fa,
                        (int)_UNK_007572fc,(int)_UNK_007572fe);
    local_c._0_1_ = 0x4c;
    FUN__text__00505000((int)_UNK_007575c0,(int)_UNK_007575c2,(int)_UNK_007575c4,
                        *(short *)(local_8 + 0x1da) + 0x24,(int)_UNK_007575c8,(int)_UNK_007575ca,
                        (int)_UNK_007575cc,(int)_UNK_007575ce);
    local_c._0_1_ = 0x4d;
    FUN__text__00505000((int)_UNK_007575d0,(int)_UNK_007575d2,(int)_UNK_007575d4,
                        *(short *)(local_8 + 0x1da) + 0x49,(int)_UNK_007575d8,(int)_UNK_007575da,
                        (int)_UNK_007575dc,(int)_UNK_007575de);
    local_c._0_1_ = 0x4e;
    FUN__text__00505000((int)_UNK_007575e0,(int)_UNK_007575e2,(int)_UNK_007575e4,
                        *(short *)(local_8 + 0x1da) + 0x6d,(int)_UNK_007575e8,(int)_UNK_007575ea,
                        (int)_UNK_007575ec,(int)_UNK_007575ee);
    local_c._0_1_ = 0x4f;
    FUN__text__00505000((int)_UNK_007575f0,(int)_UNK_007575f2,(int)_UNK_007575f4,
                        *(short *)(local_8 + 0x1da) + 0x8f,(int)_UNK_007575f8,(int)_UNK_007575fa,
                        (int)_UNK_007575fc,(int)_UNK_007575fe);
    local_c._0_1_ = 0x50;
    FUN__text__00505000((int)_UNK_00757600,(int)_UNK_00757602,(int)_UNK_00757604,
                        *(short *)(local_8 + 0x1da) + 0xb6,(int)_UNK_00757608,(int)_UNK_0075760a,
                        (int)_UNK_0075760c,(int)_UNK_0075760e);
    local_c._0_1_ = 0x51;
    FUN__text__00505000((int)_UNK_00757610,(int)_UNK_00757612,(int)_UNK_00757614,
                        *(short *)(local_8 + 0x1da) + 0xd8,(int)_UNK_00757618,(int)_UNK_0075761a,
                        (int)_UNK_0075761c,(int)_UNK_0075761e);
    local_c._0_1_ = 0x52;
    FUN__text__00505000((int)_UNK_00757620,(int)_UNK_00757622,(int)_UNK_00757624,
                        *(short *)(local_8 + 0x1da) + 0xfd,(int)_UNK_00757628,(int)_UNK_0075762a,
                        (int)_UNK_0075762c,(int)_UNK_0075762e);
    local_c._0_1_ = 0x53;
    FUN__text__00505000((int)_UNK_00757630,(int)_UNK_00757632,(int)_UNK_00757634,
                        *(short *)(local_8 + 0x1da) + 0x120,(int)_UNK_00757638,(int)_UNK_0075763a,
                        (int)_UNK_0075763c,(int)_UNK_0075763e);
    local_c._0_1_ = 0x54;
    FUN__text__00505000((int)_UNK_00757640,(int)_UNK_00757642,(int)_UNK_00757644,
                        *(short *)(local_8 + 0x1da) + 0x16d,(int)_UNK_00757648,(int)_UNK_0075764a,
                        (int)_UNK_0075764c,(int)_UNK_0075764e);
    local_c = CONCAT31(local_c._1_3_,0x55);
    FUN__text__00505000((int)_UNK_00757650,(int)_UNK_00757652,(int)_UNK_00757654,
                        *(short *)(local_8 + 0x1da) + 0x1b0,(int)_UNK_00757658,(int)_UNK_0075765a,
                        (int)_UNK_0075765c,(int)_UNK_0075765e);
  }
  if (*(char *)(local_8 + 0x17e) != '\0') {
    local_c._0_1_ = 2;
    FUN__text__00505000((int)_UNK_00757120,(int)_UNK_00757122,(int)_UNK_00757124,
                        (int)*(short *)(local_8 + 0x1dc),(int)_UNK_00757128,(int)_UNK_0075712a,
                        (int)_UNK_0075712c,(int)_UNK_0075712e);
    local_c = CONCAT31(local_c._1_3_,0x24);
    FUN__text__00505000((int)_UNK_00757340,(int)_UNK_00757342,(int)_UNK_00757344,
                        *(short *)(local_8 + 0x1dc) + 0x24,(int)_UNK_00757348,(int)_UNK_0075734a,
                        (int)_UNK_0075734c,(int)_UNK_0075734e);
  }
  if (*(char *)(local_8 + 0x17f) != '\0') {
    local_c._0_1_ = 1;
    FUN__text__00505000((int)_UNK_00757110,(int)_UNK_00757112,(int)_UNK_00757114,
                        (int)*(short *)(local_8 + 0x1de),(int)_UNK_00757118,(int)_UNK_0075711a,
                        (int)_UNK_0075711c,(int)_UNK_0075711e);
    local_c._0_1_ = 0x22;
    FUN__text__00505000((int)_UNK_00757320,(int)_UNK_00757322,(int)_UNK_00757324,
                        *(short *)(local_8 + 0x1de) + 0x24,(int)_UNK_00757328,(int)_UNK_0075732a,
                        (int)_UNK_0075732c,(int)_UNK_0075732e);
    local_c = CONCAT31(local_c._1_3_,0x23);
    FUN__text__00505000((int)_UNK_00757330,(int)_UNK_00757332,(int)_UNK_00757334,
                        *(short *)(local_8 + 0x1de) + 0x48,(int)_UNK_00757338,(int)_UNK_0075733a,
                        (int)_UNK_0075733c,(int)_UNK_0075733e);
  }
  local_8 = 0x504821;
  FUN__text__0056ce80();
  return;
}

