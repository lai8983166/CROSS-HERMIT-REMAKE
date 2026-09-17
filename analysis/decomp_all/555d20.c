
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00555d20(float *param_1,float param_2,float param_3,float param_4)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float local_50;
  float fStack_4c;
  float fStack_48;
  float fStack_44;
  float local_40;
  float fStack_3c;
  float fStack_38;
  
  local_50 = param_4 * _DAT_0080c2b0;
  fStack_4c = param_3 * _UNK_0080c2b4;
  fStack_48 = param_2 * _UNK_0080c2b8;
  fStack_44 = DAT_0080c2c0 * _UNK_0080c2bc;
  FUN__text__0055ec40(&local_50,&local_50,&local_40);
  fVar1 = (float)((uint)(local_50 * fStack_38 * fStack_4c) ^ _UNK_0080c2a4);
  fVar2 = (float)((uint)(local_40 * fStack_48 * fStack_4c) ^ _UNK_0080c2a8);
  fVar3 = (float)((uint)(local_50 * fStack_48 * fStack_4c) ^ _UNK_0080c2ac);
  *param_1 = local_40 * fStack_38 * fStack_4c +
             (float)((uint)(local_50 * fStack_48 * fStack_3c) ^ _DAT_0080c2a0);
  param_1[1] = local_40 * fStack_48 * fStack_3c + fVar1;
  param_1[2] = local_50 * fStack_38 * fStack_3c + fVar2;
  param_1[3] = local_40 * fStack_38 * fStack_3c + fVar3;
  return;
}

