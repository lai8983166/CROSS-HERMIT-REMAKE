
void FUN__text__004d29e0(undefined1 param_1,undefined2 param_2,uint param_3,undefined4 param_4,
                        short param_5,short param_6,short param_7,short param_8,short param_9,
                        short param_10,short param_11,short param_12,undefined1 param_13,
                        undefined1 param_14,undefined1 param_15,undefined1 param_16)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_3 & 0xff;
  cVar1 = (char)((ushort)param_5 >> 8);
  switch(local_c) {
  case 0:
    FUN__text__004d2ba0(CONCAT31((int3)cVar1,param_1),param_4,param_2,(int)param_5,(int)param_6);
    break;
  case 1:
    FUN__text__004d2ca0(CONCAT31((int3)cVar1,param_1),param_4,param_2,(int)param_5,(int)param_6,
                        (int)param_7,(int)param_8,(int)param_9,(int)param_10);
    break;
  case 2:
    FUN__text__004d2dd0(CONCAT31((int3)cVar1,param_1),param_4,param_2,(int)param_5,(int)param_6,
                        (int)param_7,(int)param_8,(int)param_9,(int)param_10,(int)param_11,
                        (int)param_12);
    break;
  case 3:
    FUN__text__004d3050(CONCAT31((int3)cVar1,param_1),param_4,param_2,(int)param_5,(int)param_6,
                        (int)param_7,(int)param_8,(int)param_9,(int)param_10,param_13,param_14,
                        param_15,param_16);
    break;
  case 4:
    FUN__text__004d30c0(CONCAT31((int3)cVar1,param_1),param_4,param_2,(int)param_5,(int)param_6,
                        param_13,param_14,param_15,param_16);
  }
  local_8 = 0x4d2b80;
  FUN__text__0056ce80();
  return;
}

